#!/usr/bin/env python3
"""
AI Video Reel Generator - Startup Script
========================================
This script checks dependencies and starts the Flask web application.
"""

import sys
import subprocess
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        return False
    return True

def check_package(package_name):
    """Check if a package is installed"""
    try:
        __import__(package_name)
        print(f"✅ {package_name} is already installed")
        return True
    except ImportError:
        print(f"❌ {package_name} is not installed")
        return False

def install_package(package_name):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"✅ Installed {package_name}")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package_name}")
        return False

def check_ffmpeg():
    """Check if FFmpeg is installed"""
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
    print("🎬 AI Video Reel Generator - Startup Check")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Check required packages
    required_packages = [
        'flask',
        'flask_cors', 
        'moviepy',
        'whisper_timestamped',
        'openai',
        'yt_dlp'
    ]
    
    all_packages_installed = True
    for package in required_packages:
        if not check_package(package):
            print(f"Installing {package}...")
            if not install_package(package):
                all_packages_installed = False
    
    if not all_packages_installed:
        print("❌ Some packages could not be installed")
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
    print("🚀 Starting AI Video Reel Generator...")
    print("   Open your browser to: http://localhost:5000")
    print("   Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Start the Flask app with auto-reload disabled
    try:
        from app import app
        # Disable auto-reload to prevent connection reset issues during video processing
        app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)
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