# Instagram
from instagrapi import Client
import time

def upload_to_instagram(path, caption, username, password):
    cl = Client()
    cl.login(username, password)
    time.sleep(2)
    cl.video_upload(path, caption)
    print("✅ Uploaded to Instagram")


# TikTok
from tiktok_uploader.upload import upload_video

def upload_to_tiktok(path, caption, sessionid):
    upload_video(
        path=path,
        description=caption,
        cookies={"sessionid": sessionid}
    )
    print("✅ Uploaded to TikTok")


# YouTube
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.http
import google.auth.exceptions


def upload_to_youtube(path, title, description, secrets_file):
    """
    Uploads a video to YouTube using OAuth2 credentials.
    
    Args:
        path (str): Path to the video file
        title (str): Title of the video
        description (str): Description of the video
        secrets_file (str): Path to the client secrets JSON file
    """
    print("🔑 Authenticating with YouTube API...")
    try:
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = secrets_file

        print(client_secrets_file)
        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, ["https://www.googleapis.com/auth/youtube.upload"] 
        )
        print(flow)
        credentials = flow.run_local_server(port=0)
        print(credentials)
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials
        )
        print(youtube)
        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": ["reels", "shorts", "automated"],
                "categoryId": "22"  # See YouTube categories
            },
            "status": {
                "privacyStatus": "public"
            }
        }

        # Insert request
        insert_request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=googleapiclient.http.MediaFileUpload(path)
        )

        response = insert_request.execute()
        print(f"🎥 Successfully uploaded to YouTube: {response['id']}")
        return response['id']

    except google.auth.exceptions.RefreshError:
        print("❌ YouTube authentication failed. Re-authenticate by removing old tokens.")
    except Exception as e:
        print(f"❌ YouTube upload failed: {e}")