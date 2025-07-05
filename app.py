from flask import Flask, request, jsonify, send_file, render_template, Response
from flask_cors import CORS
import os
import json
import tempfile
import shutil
from werkzeug.utils import secure_filename
import uuid
import traceback
import time
import threading
import queue

# Import your existing modules
from src.downloader import download_video, get_youtube_trending_top_video
from src.processor import extract_audio
from src.transcriber import transcribe_with_timestamps
from src.ai_analyzer import get_ai_highlights
from src.reel_editor import create_reel

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('output/reels', exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/trending', methods=['GET'])
def get_trending():
    """Get trending YouTube video"""
    try:
        trending = get_youtube_trending_top_video()
        if trending:
            return jsonify({'success': True, 'data': trending})
        else:
            return jsonify({'success': False, 'error': 'No trending videos found'})
    except Exception as e:
        print(f"Error fetching trending video: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/process', methods=['POST'])
def process_video():
    """Process video from file upload, URL, or trending video"""
    try:
        # Check if this is a file upload
        if 'file' in request.files:
            video_source = 'file'
            video_url = ''
        else:
            # Handle JSON data
            try:
                data = request.get_json()
                if not data:
                    return jsonify({'success': False, 'error': 'Invalid JSON data'})
                video_source = data.get('source')  # 'url' or 'trending'
                video_url = data.get('url', '')
            except Exception as e:
                return jsonify({'success': False, 'error': f'Invalid request format: {str(e)}'})
        
        if not video_source:
            return jsonify({'success': False, 'error': 'No video source specified'})
        
        # Generate unique session ID
        session_id = str(uuid.uuid4())
        session_folder = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
        os.makedirs(session_folder, exist_ok=True)
        
        video_path = None
        
        try:
            if video_source == 'file':
                # Handle file upload
                if 'file' not in request.files:
                    return jsonify({'success': False, 'error': 'No file uploaded'})
                
                file = request.files['file']
                if file.filename == '':
                    return jsonify({'success': False, 'error': 'No file selected'})
                
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    video_path = os.path.join(session_folder, filename)
                    file.save(video_path)
                else:
                    return jsonify({'success': False, 'error': 'Invalid file type. Supported: MP4, AVI, MOV, MKV, WEBM'})
                    
            elif video_source == 'url':
                # Download from URL
                if not video_url:
                    return jsonify({'success': False, 'error': 'No URL provided'})
                
                print("video_url------>", video_url)
                print("session_folder------>", session_folder)
                video_path = download_video(video_url, session_folder)
                
            elif video_source == 'trending':
                # Get trending video
                trending = get_youtube_trending_top_video()
                if not trending:
                    return jsonify({'success': False, 'error': 'No trending videos found'})
                
                print("trending------>", trending['url'])
                video_path = download_video(trending['url'], session_folder)
            else:
                return jsonify({'success': False, 'error': f'Invalid video source: {video_source}'})
            
        except Exception as e:
            print(f"Error in video acquisition: {str(e)}")
            print(traceback.format_exc())
            return jsonify({'success': False, 'error': f'Failed to acquire video: {str(e)}'})
        
        # Wait for file to be fully written and accessible
        if not video_path or not os.path.exists(video_path):
            return jsonify({'success': False, 'error': 'Failed to get video file'})
        
        # Add a small delay to ensure file is fully written
        time.sleep(2)
        
        # Double-check file exists and is accessible
        for _ in range(5):
            if os.path.exists(video_path) and os.path.getsize(video_path) > 0:
                break
            time.sleep(1)
        else:
            return jsonify({'success': False, 'error': 'Downloaded file not found or not accessible'})
        
        # Process the video
        try:
            result = process_video_pipeline(video_path, session_id)
            result['session_id'] = session_id
            
            return jsonify({'success': True, 'data': result})
        except Exception as e:
            print(f"Error in video processing pipeline: {str(e)}")
            print(traceback.format_exc())
            return jsonify({'success': False, 'error': f'Video processing failed: {str(e)}'})
        
    except Exception as e:
        print(f"Unexpected error in process_video: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'success': False, 'error': f'Unexpected error: {str(e)}'})

def process_video_pipeline(video_path, session_id):
    """Process video through the entire pipeline"""
    try:
        # Step 1: Extract audio
        audio_path = extract_audio(video_path, f"uploads/{session_id}")
        
        # Step 2: Transcribe with timestamps
        segments = transcribe_with_timestamps(audio_path)
        
        # Step 3: Get AI highlights
        highlights, caption = get_ai_highlights(segments)
        
        if not isinstance(highlights, list) or len(highlights) == 0:
            highlights = [{"start": 0, "end": 30}]
            caption = "Generated Reel"
        
        # Convert to tuple format
        try:
            highlight_segments = [(float(seg['start']), float(seg['end'])) for seg in highlights]
        except (KeyError, TypeError, ValueError):
            highlight_segments = [(0.0, 30.0)]
        
        # Step 4: Create reel
        reel_filename = f"reel_{session_id}.mp4"
        reel_path = create_reel(
            video_path, 
            highlight_segments, 
            caption=caption,
            output_path=f"output/reels/{reel_filename}"
        )
        
        return {
            'original_video': video_path,
            'audio_path': audio_path,
            'segments': segments[:10],  # First 10 segments for preview
            'highlights': highlights,
            'caption': caption,
            'reel_path': reel_path,
            'reel_filename': reel_filename
        }
        
    except Exception as e:
        raise Exception(f"Pipeline error: {str(e)}")

@app.route('/api/download/<session_id>/<filename>')
def download_reel(session_id, filename):
    """Download the generated reel"""
    try:
        file_path = os.path.join('output/reels', filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'success': False, 'error': 'File not found'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def sse_format(data, event=None):
    """Format data as SSE event."""
    msg = ''
    if event:
        msg += f'event: {event}\n'
    msg += f'data: {json.dumps(data)}\n\n'
    return msg

@app.route('/api/upload/stream', methods=['POST'])
def upload_to_platforms_stream():
    data = request.get_json()
    reel_path = data.get('reel_path')
    caption = data.get('caption', 'Generated using AI!')
    platforms = data.get('platforms', [])
    def generate():
        try:
            # Load secrets
            try:
                with open('config/secrets.json') as f:
                    secrets = json.load(f)
            except:
                secrets = {}
            for platform in platforms:
                try:
                    if platform == 'instagram' and 'instagram' in secrets:
                        from src.uploader import upload_to_instagram
                        ig_secrets = secrets["instagram"]
                        upload_to_instagram(reel_path, caption, ig_secrets["username"], ig_secrets["password"])
                        yield sse_format({'platform': 'instagram', 'success': True, 'message': 'Uploaded to Instagram'}, event='upload')
                    elif platform == 'tiktok' and 'tiktok' in secrets:
                        from src.uploader import upload_to_tiktok
                        tiktok_secrets = secrets["tiktok"]
                        upload_to_tiktok(reel_path, caption, tiktok_secrets["sessionid"])
                        yield sse_format({'platform': 'tiktok', 'success': True, 'message': 'Uploaded to TikTok'}, event='upload')
                    elif platform == 'youtube':
                        from src.uploader import upload_to_youtube
                        yt_secrets_path = "config/youtube_secrets.json"
                        upload_to_youtube(reel_path, caption, "Generated using AI from trending YouTube content.", yt_secrets_path)
                        yield sse_format({'platform': 'youtube', 'success': True, 'message': 'Uploaded to YouTube'}, event='upload')
                    else:
                        yield sse_format({'platform': platform, 'success': False, 'error': 'Credentials not found'}, event='upload')
                except Exception as e:
                    yield sse_format({'platform': platform, 'success': False, 'error': str(e)}, event='upload')
            # Signal completion
            yield sse_format({'done': True}, event='done')
            import sys, time
            sys.stdout.flush()
            time.sleep(0.5)  # Ensure client receives the last event
        except Exception as e:
            yield sse_format({'success': False, 'error': str(e)}, event='error')
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    # Disable auto-reload to prevent connection reset issues during video processing
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000) 