#!/usr/bin/env python3
"""
AI Video Reel Generator - Startup Script
"""

import os
import sys
import subprocess
import importlib.util

def check_dependency(module_name, package_name=None):
    """Check if a Python module is installed"""
    if package_name is None:
        package_name = module_name
    
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        print(f"❌ {package_name} is not installed. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"✅ {package_name} installed successfully!")
            return True
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package_name}")
            return False
    else:
        print(f"✅ {package_name} is already installed")
        return True

def check_ffmpeg():
    """Check if FFmpeg is installed"""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        print("✅ FFmpeg is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ FFmpeg is not installed or not in PATH")
        print("Please install FFmpeg:")
        print("  Windows: Download from https://ffmpeg.org/download.html")
        print("  macOS: brew install ffmpeg")
        print("  Linux: sudo apt install ffmpeg")
        return False

def check_env_file():
    """Check if .env file exists"""
    if not os.path.exists('.env'):
        print("⚠️  .env file not found. Creating template...")
        with open('.env', 'w') as f:
            f.write("""# AI Video Reel Generator Environment Variables
OPENROUTER_AI_KEY=your_openrouter_api_key_here
FLASK_ENV=development
FLASK_DEBUG=1

# Get your OpenRouter API key from: https://openrouter.ai/
""")
        print("✅ Created .env template. Please add your OpenRouter API key!")
        return False
    else:
        print("✅ .env file found")
        return True

def main():
    """Main startup function"""
    print("🎬 AI Video Reel Generator - Startup Check")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Check critical dependencies
    critical_deps = [
        ('flask', 'flask'),
        ('flask_cors', 'flask-cors'),
        ('moviepy', 'moviepy'),
        ('whisper_timestamped', 'whisper-timestamped'),
        ('openai', 'openai'),
        ('yt_dlp', 'yt-dlp'),
    ]
    
    all_good = True
    for module, package in critical_deps:
        if not check_dependency(module, package):
            all_good = False
    
    # Check FFmpeg
    if not check_ffmpeg():
        all_good = False
    
    # Check environment file
    env_ok = check_env_file()
    
    print("\n" + "=" * 50)
    
    if not all_good:
        print("❌ Some dependencies are missing. Please install them and try again.")
        sys.exit(1)
    
    if not env_ok:
        print("⚠️  Please configure your .env file with your OpenRouter API key")
        print("   You can still run the app, but AI features won't work without the API key")
    
    print("🚀 Starting AI Video Reel Generator...")
    print("   Open your browser to: http://localhost:5000")
    print("   Press Ctrl+C to stop the server")
    print("\n" + "=" * 50)
    
    # Import and run the Flask app
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except ImportError as e:
        print(f"❌ Error importing app: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error running app: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 