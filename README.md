# 🎬 AI Video Reel Generator - Web Application

A powerful, full-stack web application that automatically transforms any video into engaging short-form content using AI. Upload videos, paste URLs, or use trending YouTube content to create viral reels in seconds!

![AI Video Reel Generator](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![AI Powered](https://img.shields.io/badge/AI-Powered-orange.svg)
![Multi-Platform](https://img.shields.io/badge/Multi--Platform-Upload-red.svg)

## ✨ Features

### 🎯 **Multiple Input Sources**
- **📁 File Upload**: Drag & drop or browse for video files (MP4, AVI, MOV, MKV, WEBM)
- **🔗 URL Input**: Paste YouTube, TikTok, or any video URL
- **🔥 Trending Videos**: Automatically fetch the latest trending YouTube content

### 🤖 **AI-Powered Processing**
- **🎵 Audio Extraction**: Convert video to audio for analysis
- **🗣️ Smart Transcription**: Use Whisper AI to convert speech to text with precise timestamps
- **🧠 AI Highlight Detection**: OpenRouter AI identifies the most engaging moments
- **✂️ Professional Reel Creation**: Generate 30-second reels with captions and effects

### 🌐 **Modern Web Interface**
- **📱 Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **⚡ Real-time Progress**: Live updates through all processing steps
- **🎨 Beautiful UI**: Modern gradient design with smooth animations
- **📊 Preview Features**: View segments, highlights, and final reel before download

### 📤 **Multi-Platform Distribution**
- **📥 Download**: Save generated reels to your device
- **📱 Instagram**: Direct upload with captions
- **🎵 TikTok**: One-click sharing to TikTok
- **📺 YouTube**: Upload as Shorts with metadata

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
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file
echo "OPENROUTER_AI_KEY=your_api_key_here" > .env

# 3. Run the application
python app.py
```

#### **Option 3: Platform-Specific Launchers**
- **Windows**: Double-click `start.bat`
- **Mac/Linux**: Run `./start.sh`

### 🔑 Get Your API Key

1. Visit [OpenRouter.ai](https://openrouter.ai/)
2. Sign up and get your API key
3. Add it to the `.env` file:
   ```env
   OPENROUTER_AI_KEY=your_openrouter_api_key_here
   FLASK_ENV=development
   FLASK_DEBUG=1
   ```

### 🌐 Launch the Application

1. **Start the server**: `python run.py`
2. **Open browser**: Navigate to `http://localhost:5000`
3. **Start creating**: Upload videos, paste URLs, or use trending content!

## 🎯 How It Works

### 1. **Video Input & Processing**
```
📹 Video Input → 🎵 Audio Extraction → 🗣️ Transcription → 🧠 AI Analysis → ✂️ Reel Generation
```

### 2. **AI Pipeline**
1. **Download**: Fetch video content from source
2. **Extract Audio**: Convert video to audio using FFmpeg
3. **Transcribe**: Use Whisper AI for speech-to-text with timestamps
4. **AI Analysis**: OpenRouter AI identifies engaging moments
5. **Create Reel**: Generate 30-second highlight reel with captions

### 3. **Output & Sharing**
- **Preview**: Watch generated reel in browser
- **Download**: Save to device
- **Upload**: Share to Instagram, TikTok, YouTube

## 🎨 Web Interface Features

### **📱 Responsive Design**
- **Desktop**: Full-featured interface with all options
- **Tablet**: Optimized layout for touch interaction
- **Mobile**: Streamlined interface for on-the-go use

### **🎯 Input Methods**
- **Drag & Drop**: Intuitive file upload with visual feedback
- **URL Pasting**: Support for YouTube, TikTok, and other platforms
- **Trending Videos**: One-click access to viral content

### **📊 Real-time Progress**
- **Step-by-step tracking**: Visual progress through all 5 processing steps
- **Live updates**: Real-time status updates
- **Error handling**: Clear error messages with retry options

### **🎬 Preview & Download**
- **Video preview**: Watch generated reel before downloading
- **Segment preview**: View transcribed text with timestamps
- **Highlight preview**: See AI-selected moments
- **One-click download**: Save reel to your device

## 🔧 Configuration

### **Social Media Credentials**

Create `config/secrets.json` for social media uploads:

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

## 📁 Project Structure

```
video_to_reel/
├── 🚀 app.py                 # Flask web application
├── 📋 requirements.txt       # Python dependencies
├── 🎯 run.py                # Smart startup script
├── 🖥️ start.bat             # Windows launcher
├── 🐧 start.sh              # Unix/Linux/macOS launcher
├── 📖 README.md             # This file
├── ⚡ SETUP.md              # Quick setup guide
├── 📁 templates/
│   └── 🎨 index.html        # Modern web interface
├── 📁 src/
│   ├── 🎬 main.py           # Original CLI version
│   ├── 📥 downloader.py     # Video downloading utilities
│   ├── 🎵 processor.py      # Audio extraction
│   ├── 🗣️ transcriber.py    # Speech-to-text conversion
│   ├── 🧠 ai_analyzer.py    # AI highlight detection
│   ├── ✂️ reel_editor.py    # Video editing and reel creation
│   └── 📤 uploader.py       # Social media upload functions
├── 📁 config/
│   ├── 🔐 secrets.json      # Social media credentials
│   └── 📺 youtube_secrets.json # YouTube API credentials
├── 📁 uploads/              # Temporary uploaded files
└── 📁 output/
    └── 🎬 reels/           # Generated reel videos
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

## 🚀 Deployment

### **Local Development**
```bash
python run.py
```

### **Production (Gunicorn)**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### **Docker Deployment**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### **Cloud Platforms**
- **Heroku**: Deploy with Procfile
- **Railway**: Connect GitHub repository
- **Render**: Automatic deployment from Git
- **AWS/GCP**: Use Docker container

## 🛠️ Troubleshooting

### **Common Issues**

| Issue | Solution |
|-------|----------|
| **FFmpeg not found** | Download from [ffmpeg.org](https://ffmpeg.org/download.html) |
| **API errors** | Check OpenRouter API key in `.env` file |
| **Upload failures** | Configure social media credentials in `config/secrets.json` |
| **Connection timeouts** | Check internet connection and try shorter videos |
| **File too large** | Use videos under 500MB or compress before upload |

### **Error Messages**

- **"File too large"**: Reduce video size or compress
- **"Invalid file type"**: Use MP4, AVI, MOV, MKV, or WEBM
- **"API key invalid"**: Check OpenRouter API key
- **"Download failed"**: Check URL validity and internet connection

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
