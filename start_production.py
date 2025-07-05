#!/usr/bin/env python3
"""
AI Video Reel Generator - Production Startup Script
==================================================
This script starts the Flask app using waitress for production use.
"""

import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'flask',
        'flask_cors', 
        'moviepy',
        'whisper_timestamped',
        'openai',
        'yt_dlp',
        'waitress'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Install them with: pip install " + " ".join(missing_packages))
        return False
    
    return True

def check_ffmpeg():
    """Check if FFmpeg is installed"""
    import subprocess
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ FFmpeg is installed")
            return True
        else:
            print("❌ FFmpeg is not installed")
            return False
    except FileNotFoundError:
        print("❌ FFmpeg is not installed")
        return False

def check_env_file():
    """Check if .env file exists"""
    if os.path.exists('.env'):
        print("✅ .env file found")
        return True
    else:
        print("❌ .env file not found")
        return False

def main():
    """Main startup function"""
    print("🎬 AI Video Reel Generator - Production Startup")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Check FFmpeg
    if not check_ffmpeg():
        print("⚠️  FFmpeg is required for video processing. Please install it manually.")
        print("   Windows: Download from https://ffmpeg.org/download.html")
        print("   macOS: brew install ffmpeg")
        print("   Linux: sudo apt install ffmpeg")
        return False
    
    # Check .env file
    if not check_env_file():
        print("⚠️  .env file not found. Please create one with your API keys.")
        print("   Required keys: OPENAI_API_KEY")
        return False
    
    print("=" * 50)
    print("🚀 Starting AI Video Reel Generator in production mode...")
    print("   Open your browser to: http://localhost:8080")
    print("   Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Start the Flask app with waitress
    try:
        from app import app
        from waitress import serve
        
        # Create necessary directories
        os.makedirs('uploads', exist_ok=True)
        os.makedirs('output/reels', exist_ok=True)
        os.makedirs('input/raw_videos', exist_ok=True)
        
        # Serve with waitress (production WSGI server)
        serve(app, host='0.0.0.0', port=8080, threads=4)
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 