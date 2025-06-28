import json
import os
import time
from downloader import download_video, get_youtube_trending_urls, get_youtube_trending_top_video
from processor import extract_audio
from transcriber import transcribe_with_timestamps
from ai_analyzer import get_ai_highlights   
from reel_editor import create_reel
from uploader import upload_to_instagram, upload_to_youtube, upload_to_tiktok

# Load secrets
with open('config/secrets.json') as f:
    secrets = json.load(f)

if __name__ == "__main__":
    print("🌐 Fetching trending YouTube videos...")
    # trending_urls = get_youtube_trending_urls(max_videos=1)
    trending_urls = get_youtube_trending_top_video()
    print("trending_urls---->", trending_urls)
    if not trending_urls:
        raise Exception("❌ No trending videos found.")

    # VIDEO_URL = trending_urls[0]
    VIDEO_URL = trending_urls['url']
    print(f"📹 Selected trending video: {VIDEO_URL}") 
    
    print("📥 Downloading video...")
    video_path = download_video(VIDEO_URL)

    print("🔊 Extracting audio...")
    audio_path = extract_audio(video_path)

    print("🗣️ Converting audio to text with timestamps...")
    segments = transcribe_with_timestamps(audio_path)
    # print("Segments-----", segments)

    print("🧠 Asking AI to find highlights...")
    highlights, caption = get_ai_highlights(segments)

    if not isinstance(highlights, list) or len(highlights) == 0:
        print("⚠️ AI didn't return valid highlights. Falling back to first 30 seconds.")
        highlights = [{"start": 0, "end": 30}]
        caption = "Trending Reel"

    # Convert dict list to tuple list
    try:
        highlight_segments = [(float(seg['start']), float(seg['end'])) for seg in highlights]
    except (KeyError, TypeError, ValueError) as e:
        print(f"❌ Error extracting segment times: {e}")
        highlight_segments = [(0.0, 30.0)]

    print(f"📌 Highlights selected by AI: {highlight_segments}")
    print(f"📝 Caption: {caption}")

    print("✂️ Creating reel...")
    reel_path = create_reel(video_path, highlight_segments, caption=caption)


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