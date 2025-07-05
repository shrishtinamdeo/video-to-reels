# 🎬 AI Video Reel Generator

An intelligent web application that automatically generates short video reels from trending YouTube videos using AI. The system downloads trending videos, extracts audio, transcribes speech with timestamps, uses AI to find highlights, creates engaging reels, and uploads them to social media platforms.

## ✨ Features

### 🎥 Video Processing
- **Multiple Input Sources**: Upload local videos, paste YouTube URLs, or use trending videos
- **Smart Download**: Robust YouTube video downloading with fallback methods
- **Audio Extraction**: High-quality audio extraction for transcription
- **AI-Powered Highlights**: Intelligent selection of the most engaging moments

### 🤖 AI Integration
- **Speech Transcription**: Accurate speech-to-text with timestamps using Whisper
- **Content Analysis**: OpenAI-powered analysis to identify viral moments
- **Caption Generation**: AI-generated engaging captions for social media

### 🎬 Reel Creation
- **Automatic Editing**: Seamless compilation of highlight segments
- **Professional Quality**: High-resolution output optimized for social media
- **Custom Captions**: Overlay text with engaging captions
- **Thumbnail Generation**: Automatic thumbnail creation

### 📱 Social Media Upload
- **Multi-Platform Support**: Instagram, TikTok, YouTube
- **Automated Upload**: Direct upload to social media platforms
- **Scheduled Publishing**: Queue videos for optimal posting times

### 🌐 Web Interface
- **Modern UI**: Responsive, professional web interface
- **Real-time Progress**: Live progress tracking during processing
- **Preview System**: Preview segments and highlights before final creation
- **Drag & Drop**: Easy file upload with drag-and-drop support

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** from [python.org](https://python.org)
- **FFmpeg** from [ffmpeg.org](https://ffmpeg.org/download.html)
- **OpenRouter API Key** from [openrouter.ai](https://openrouter.ai/)

### 🛠️ Installation

#### **Option 1: Automatic Setup (Recommended)**
```bash
# Clone the repository
git clone <repository-url>
cd video_to_reel

# Run the smart startup script
python run.py
```

#### **Option 2: Manual Setup**

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd video_to_reel
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install FFmpeg**
   - **Windows**: Download from [FFmpeg.org](https://ffmpeg.org/download.html)
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg`

4. **Configure environment**
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   ```

### Running the Application

#### 🛠️ Development Mode (with auto-reload disabled)
```bash
# Windows
python run.py

# Linux/macOS
python3 run.py
```

#### 🚀 Production Mode (Recommended for video processing)
```bash
# Windows
start_production.bat
# or
python start_production.py

# Linux/macOS
python3 start_production.py
```

**Important**: Use **Production Mode** for video processing to avoid connection reset issues!

## 📖 Usage

### 1. Web Interface
1. Open your browser to `http://localhost:5000` (dev) or `http://localhost:8080` (production)
2. Choose your input method:
   - **File Upload**: Drag and drop or select a video file
   - **URL Input**: Paste a YouTube video URL
   - **Trending Videos**: Use the latest trending YouTube video

### 2. Processing Pipeline
1. **Download**: Video is downloaded and prepared
2. **Audio Extraction**: Audio is extracted for transcription
3. **Transcription**: Speech is transcribed with timestamps
4. **AI Analysis**: AI identifies the most engaging moments
5. **Reel Creation**: Highlights are compiled into a short reel
6. **Upload**: Option to upload to social media platforms

### 3. Social Media Upload
- **Instagram**: Requires username/password in `config/secrets.json`
- **TikTok**: Requires session ID in `config/secrets.json`
- **YouTube**: Requires OAuth credentials in `config/youtube_secrets.json`

## 🔧 Configuration

### Environment Variables (.env)
```env
OPENAI_API_KEY=your_openai_api_key_here
FLASK_ENV=development
FLASK_DEBUG=1
```

### Social Media Secrets (config/secrets.json)
```json
{
  "instagram": {
    "username": "your_instagram_username",
    "password": "your_instagram_password"
  },
  "tiktok": {
    "sessionid": "your_tiktok_session_id"
  }
}
```

### **YouTube API Setup**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable YouTube Data API v3
4. Create OAuth 2.0 credentials
5. Download JSON file as `config/youtube_secrets.json`

## 🛠️ Troubleshooting

### Connection Reset Issues
**Problem**: `net::ERR_CONNECTION_RESET` after video download
**Solution**: 
- Use **Production Mode** (`python start_production.py`) instead of development mode
- This prevents Flask auto-reload from interrupting long video processing tasks

### Video Download Failures
**Problem**: yt-dlp download errors
**Solution**:
- The system automatically tries multiple fallback methods
- Check your internet connection
- Some videos may be region-restricted

### FFmpeg Errors
**Problem**: "FFmpeg not found" errors
**Solution**:
- Ensure FFmpeg is installed and in your system PATH
- Restart your terminal after installation

### OpenAI API Errors
**Problem**: "OpenAI API key not found" errors
**Solution**:
- Check your `.env` file has the correct `OPENAI_API_KEY`
- Ensure you have sufficient API credits

### Memory Issues
**Problem**: Out of memory during video processing
**Solution**:
- Close other applications to free up RAM
- Process shorter videos first
- Consider upgrading your system RAM

## 📁 Project Structure

```
video_to_reel/
├── app.py                 # Main Flask application
├── run.py                 # Development startup script
├── start_production.py    # Production startup script
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── templates/             # HTML templates
│   └── index.html        # Main web interface
├── src/                   # Core processing modules
│   ├── downloader.py     # Video downloading
│   ├── processor.py      # Video processing
│   ├── transcriber.py    # Speech transcription
│   ├── ai_analyzer.py    # AI analysis
│   ├── reel_editor.py    # Reel creation
│   └── uploader.py       # Social media upload
├── config/               # Configuration files
│   ├── secrets.json      # Social media credentials
│   └── youtube_secrets.json
├── uploads/              # Temporary upload storage
├── output/               # Generated reels
│   └── reels/
└── input/                # Input video storage
    └── raw_videos/
```


## 🎯 Usage Examples

### **📁 File Upload**
1. Click "Upload File" tab
2. Drag & drop video file or click to browse
3. Watch real-time progress through all steps
4. Preview and download your generated reel

### **🔗 URL Processing**
1. Click "Video URL" tab
2. Paste YouTube, TikTok, or any video URL
3. Click "Process Video"
4. AI will analyze and create highlights

### **🔥 Trending Videos**
1. Click "Trending" tab
2. View current trending YouTube video
3. Click "Generate from Trending"
4. Get instant viral content

### **📤 Social Media Upload**
1. Generate your reel
2. Select platforms (Instagram, TikTok, YouTube)
3. Click "Upload Selected Platforms"
4. Share your content instantly!

## 🔒 Security & Privacy

- **🔐 Secure Storage**: API keys stored in environment variables
- **🗑️ Temporary Files**: Uploaded files automatically cleaned up
- **🔒 HTTPS Ready**: Production deployment support
- **👤 User Sessions**: Unique session IDs for each user

## 🔄 Development vs Production

### Development Mode (`run.py`)
- ✅ Auto-reload disabled to prevent connection resets
- ✅ Debug mode enabled
- ✅ Good for testing and development
- ❌ Not recommended for video processing

### Production Mode (`start_production.py`)
- ✅ Uses Waitress WSGI server
- ✅ Stable for long-running video processing
- ✅ Better error handling
- ✅ Recommended for actual video processing
- ✅ Runs on port 8080

## 🚀 Deployment

### Local Production
```bash
python start_production.py
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Copy application
COPY . /app
WORKDIR /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose port
EXPOSE 8080

# Start production server
CMD ["python", "start_production.py"]
```

### Cloud Deployment
- **Heroku**: Use the provided `Procfile`
- **AWS**: Deploy with Elastic Beanstalk
- **Google Cloud**: Use App Engine or Compute Engine
- **Azure**: Deploy with App Service

## 📈 Performance Tips

- **🎬 Video Length**: Shorter videos process faster
- **📊 File Size**: Keep videos under 500MB for best performance
- **🌐 Internet**: Stable connection for URL downloads
- **💾 Storage**: Ensure sufficient disk space for processing

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### **Development Setup**
```bash
# Clone and setup
git clone <repository-url>
cd video_to_reel
pip install -r requirements.txt

# Run in development mode
python app.py
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[OpenRouter](https://openrouter.ai/)** for AI analysis capabilities
- **[Whisper](https://github.com/openai/whisper)** for speech recognition
- **[MoviePy](https://zulko.github.io/moviepy/)** for video processing
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** for video downloading
- **[Flask](https://flask.palletsprojects.com/)** for web framework

## 📞 Support & Community

### **Getting Help**
- 📖 **Documentation**: Check this README and `SETUP.md`
- 🐛 **Issues**: Report bugs on GitHub Issues
- 💬 **Discussions**: Join community discussions
- 📧 **Email**: Contact for business inquiries

### **Feature Requests**
- 🚀 **New Features**: Suggest new capabilities
- 🔧 **Improvements**: Propose enhancements
- 🎨 **UI/UX**: Share design ideas

---

## 🎉 Success Stories

> *"This tool saved me hours of manual video editing. The AI perfectly identifies the best moments!"* - Content Creator

> *"The web interface is so intuitive. I can create viral reels in minutes!"* - Social Media Manager

> *"Finally, a tool that actually understands what makes content engaging!"* - Digital Marketer

---

**🎬 Made with ❤️ for content creators everywhere!**

*Transform your videos into viral content with the power of AI.*
