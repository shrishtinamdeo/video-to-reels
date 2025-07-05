import yt_dlp
import subprocess
import os
from bs4 import BeautifulSoup
import requests
import re
import json
import time

def download_video(url, output_dir="input/raw_videos"):
    """
    Download a single video using its URL with robust error handling.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # More robust yt-dlp options to handle format issues and timeouts
    ydl_opts = {
        'format': 'best[height<=720]/best[ext=mp4]/best',  # Prefer 720p or lower, then mp4, then best
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'retries': 5,  # Increased retries
        'fragment_retries': 5,
        'skip_unavailable_fragments': True,
        'extractor_retries': 5,
        'socket_timeout': 60,  # Increased timeout
        'http_chunk_size': 10485760,  # 10MB chunks
        'max_sleep_interval': 30,  # Maximum sleep between retries
        'sleep_interval': 5,  # Sleep between retries
        'max_downloads': 1,  # Only download one video
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"📥 Attempting to download: {url}")
            
            # First try to extract info without downloading
            try:
                info = ydl.extract_info(url, download=False)
                if not info:
                    raise Exception("Could not extract video information")
                
                # Check if video is available
                if info.get('_type') == 'playlist':
                    # Handle playlist - take first video
                    if 'entries' in info and info['entries']:
                        info = info['entries'][0]
                    else:
                        raise Exception("No videos found in playlist")
                
                # Now download with the extracted info
                ydl.download([url])
                
                # Get the filename
                video_path = ydl.prepare_filename(info)
                
                # Check if file exists and wait for it to be fully written
                for attempt in range(10):
                    if os.path.exists(video_path) and os.path.getsize(video_path) > 0:
                        print(f"✅ Successfully downloaded: {os.path.basename(video_path)}")
                        return video_path
                    time.sleep(1)
                
                # Try to find the file with different extensions
                base_path = os.path.splitext(video_path)[0]
                for ext in ['.mp4', '.webm', '.mkv', '.avi', '.mov']:
                    alt_path = base_path + ext
                    if os.path.exists(alt_path) and os.path.getsize(alt_path) > 0:
                        print(f"✅ Found downloaded file: {os.path.basename(alt_path)}")
                        return alt_path
                
                raise Exception("Downloaded file not found or empty")
                    
            except Exception as e:
                print(f"⚠️ First attempt failed: {str(e)}")
                
                # Fallback: try with different format options
                print("🔄 Trying fallback download method...")
                ydl_opts_fallback = {
                    'format': 'worst[ext=mp4]/worst',  # Try worst quality first
                    'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
                    'quiet': True,
                    'no_warnings': True,
                    'ignoreerrors': True,
                    'retries': 8,  # More retries for fallback
                    'fragment_retries': 8,
                    'skip_unavailable_fragments': True,
                    'extractor_retries': 8,
                    'socket_timeout': 90,  # Longer timeout
                    'max_sleep_interval': 60,
                    'sleep_interval': 10,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts_fallback) as ydl2:
                    info = ydl2.extract_info(url, download=True)
                    video_path = ydl2.prepare_filename(info)
                    
                    # Wait for file to be fully written
                    for attempt in range(15):
                        if os.path.exists(video_path) and os.path.getsize(video_path) > 0:
                            print(f"✅ Fallback download successful: {os.path.basename(video_path)}")
                            return video_path
                        time.sleep(1)
                    
                    raise Exception("Fallback download completed but file not accessible")
                        
    except Exception as e:
        print(f"❌ yt-dlp download failed: {str(e)}")
        
        # Final fallback: try with pytube if it's a YouTube URL
        if 'youtube.com' in url or 'youtu.be' in url:
            print("🔄 Trying pytube fallback for YouTube...")
            try:
                return download_with_pytube(url, output_dir)
            except Exception as pytube_error:
                print(f"❌ pytube fallback also failed: {str(pytube_error)}")
        
        raise Exception(f"All download methods failed: {str(e)}")

def download_with_pytube(url, output_dir):
    """
    Fallback download method using pytube for YouTube videos.
    """
    try:
        from pytube import YouTube
        
        print(f"📥 Downloading with pytube: {url}")
        yt = YouTube(url)
        
        # Get the best available stream
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        
        if not stream:
            # Fallback to any available stream
            stream = yt.streams.filter(file_extension='mp4').first()
        
        if not stream:
            raise Exception("No suitable stream found")
        
        # Download the video
        filename = f"{yt.title}.mp4"
        # Clean filename for filesystem
        filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = filename.replace(' ', '_')
        
        file_path = os.path.join(output_dir, filename)
        stream.download(output_path=output_dir, filename=filename)
        
        # Wait for file to be fully written
        for attempt in range(10):
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                print(f"✅ pytube download successful: {filename}")
                return file_path
            time.sleep(1)
        
        raise Exception("pytube download completed but file not accessible")
            
    except ImportError:
        raise Exception("pytube not installed. Install with: pip install pytube")
    except Exception as e:
        raise Exception(f"pytube download failed: {str(e)}")

def get_youtube_trending_top_video():
    """
    Fetches the top trending YouTube video using yt-dlp.
    Returns title, url, views, and channel.
    """
    try:
        print("🌐 Fetching trending videos via yt-dlp...")
        
        # Updated yt-dlp command with better options and timeout handling
        cmd = [
            "yt-dlp",
            "--flat-playlist",
            "--dump-json",
            "--no-warnings",
            "--ignore-errors",
            "--max-downloads", "5",  # Limit to 5 videos
            "--socket-timeout", "30",  # Add socket timeout
            "--retries", "3",  # Add retries
            "https://www.youtube.com/feed/trending"
        ]
        
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=90,  # Increased timeout
            check=True
        )

        if not result.stdout.strip():
            raise ValueError("Empty output from yt-dlp")

        # Parse output line by line (each line is a separate JSON object)
        videos = []
        for line in result.stdout.strip().split('\n'):
            try:
                video_info = json.loads(line)
                if 'url' in video_info and 'title' in video_info:
                    videos.append(video_info)
            except json.JSONDecodeError as e:
                continue  # Skip invalid lines

        if videos:
            # Try to get the first valid video
            for video in videos[:3]:  # Check first 3 videos
                try:
                    title = video.get('title', 'No Title')
                    url = video.get('url', '')
                    view_count = video.get('view_count', 'N/A')
                    channel = video.get('channel', 'Unknown')
                    
                    if url and title:
                        print(f"✅ Top trending video: {title} | Views: {view_count} | Channel: {channel}")
                        return {
                            'title': title,
                            'url': url,
                            'views': view_count,
                            'channel': channel
                        }
                except Exception as e:
                    print(f"⚠️ Error processing video: {str(e)}")
                    continue
            
            raise Exception("No valid trending videos found")
        else:
            raise Exception("No trending videos found")
            
    except subprocess.TimeoutExpired:
        print("❌ Timeout while fetching trending videos")
        raise Exception("Timeout while fetching trending videos")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running yt-dlp: {e.stderr}")
        raise Exception(f"yt-dlp error: {e.stderr}")
    except Exception as e:
        print(f"❌ Error fetching trending videos: {str(e)}")
        raise Exception(f"Failed to fetch trending videos: {str(e)}")

def get_youtube_trending_urls(max_videos=1):
    """
    Fetch trending YouTube video URLs by parsing embedded JSON in script tags.
    """
    url = "https://www.youtube.com/feed/trending" 
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    # print("Response----->", response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    # print("soup---->", soup)

    # Find all script tags and look for the one containing trending video data
    scripts = soup.find_all("script")
    pattern = re.compile(r"var ytInitialData = ({.*});", re.DOTALL)

    for script in scripts:
        if script.string and pattern.search(script.string):
            data_str = pattern.search(script.string).group(1)
            data = json.loads(data_str)

            # Navigate to trending videos section
            try:
                trending_videos = (
                    data["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][0]
                    ["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]
                    ["itemSectionRenderer"]["contents"][0]["shelfRenderer"]
                    ["content"]["expandedShelfContentsRenderer"]["items"]
                )

                urls = []
                for item in trending_videos:
                    if "videoRenderer" in item:
                        video_id = item["videoRenderer"]["videoId"]
                        urls.append(f"https://www.youtube.com/watch?v={video_id}")

                    if len(urls) >= max_videos:
                        break

                print(f"🔍 Found {len(urls)} trending videos.")
                return urls

            except KeyError as e:
                print(f"❌ Failed to parse YouTube trending JSON: missing key {e}")
                return []

    print("❌ Could not find trending video data in page source.")
    return []