import yt_dlp
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