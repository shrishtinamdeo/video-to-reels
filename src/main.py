import json
import os
from downloader import download_video
from processor import extract_audio
from ai_analyzer import detect_scenes, find_audio_peaks
from reel_editor import create_reel
from uploader import upload_to_instagram, upload_to_youtube, upload_to_tiktok

# Load secrets
with open('config/secrets.json') as f:
    secrets = json.load(f)

# Input
VIDEO_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

if __name__ == "__main__":
    print("📥 Downloading video...")
    video_path = download_video(VIDEO_URL)

    print("🔊 Extracting audio...")
    audio_path = extract_audio(video_path)

    print("🔍 Detecting scenes...")
    scenes = detect_scenes(video_path)

    if not scenes:
        print("⚠️ No scenes detected. Using fallback: first 30 seconds.")
        scenes = [(0, 30)]

    print("✂️ Creating reel...")
    reel_path = create_reel(video_path, scenes)

    print("📤 Uploading to platforms...")

    # Instagram 
    print("🎥 Uploading to Instagram...")
    # ig_secrets = secrets["instagram"]
    # upload_to_instagram(reel_path, "Automated reel from trending video!", ig_secrets["username"], ig_secrets["password"])

    # TikTok
    print("🎥 Uploading to TikTok...")
    # tiktok_secrets = secrets["tiktok"]
    # upload_to_tiktok(reel_path, "Automated reel from trending video!", tiktok_secrets["sessionid"])

    # YouTube
    print("🎥 Uploading to YouTube...")
    # yt_secrets_path = "config/youtube_secrets.json"
    # upload_to_youtube(reel_path, "Automated reel from trending video!", "Generated using AI from trending YouTube content.", yt_secrets_path)

    print("✅ Done!")