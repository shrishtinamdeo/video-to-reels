import yt_dlp
import subprocess
import os
from bs4 import BeautifulSoup
import requests
import re
import json

def download_video(url, output_dir="input/raw_videos"):
    """
    Download a single video using its URL.
    """
    os.makedirs(output_dir, exist_ok=True)
    ydl_opts = {
        'format': 'best',
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        video_path = ydl.prepare_filename(info)
        return video_path

def get_youtube_trending_top_video():
    """
    Fetches the top trending YouTube video using yt-dlp.
    Returns title, url, views, and channel.
    """
    try:
        print("🌐 Fetching trending videos via yt-dlp...")
        # Run yt-dlp command to fetch trending feed
        result = subprocess.run(
            ["yt-dlp", "--flat-playlist", "--dump-json", "https://www.youtube.com/feed/trending"], 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )

        if not result.stdout.strip():
            raise ValueError("Empty output from yt-dlp")

        # Parse output line by line (each line is a separate JSON object)
        videos = []
        for line in result.stdout.strip().split('\n'):
            try:
                video_info = json.loads(line)
                if 'url' in video_info:
                    videos.append(video_info)
            except json.JSONDecodeError as e:
                continue  # Skip invalid lines

        if videos:
            top_video = videos[0]
            title = top_video.get('title', 'No Title')
            url = top_video.get('url', '')
            view_count = top_video.get('view_count', 'N/A')
            channel = top_video.get('channel', 'Unknown')

            print(f"✅ Top trending video: {title} | Views: {view_count} | Channel: {channel}")
            return {
                'title': title,
                'url': url,
                'views': view_count,
                'channel': channel
            }
        else:
            print("❌ No trending videos found.")
            return {}

    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed with error: {e.stderr}")
        return {}
    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")
        return {}

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