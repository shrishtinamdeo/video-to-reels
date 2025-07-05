# 🚀 Quick Setup Guide

## Windows Users
1. Double-click `start.bat` or run:
   ```cmd
   python run.py
   ```

## Mac/Linux Users
1. Make the script executable: `chmod +x start.sh`
2. Run: `./start.sh` or `python3 run.py`

## Manual Setup
1. Install Python 3.8+ from [python.org](https://python.org)
2. Install FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
3. Run: `pip install -r requirements.txt`
4. Create `.env` file with your OpenRouter API key
5. Run: `python app.py`

## Get Your API Key
1. Go to [OpenRouter.ai](https://openrouter.ai/)
2. Sign up and get your API key
3. Add it to the `.env` file:
   ```
   OPENROUTER_AI_KEY=your_key_here
   ```

## Open the App
Navigate to: http://localhost:5000

## Features Available
- ✅ Upload video files (drag & drop)
- ✅ Paste video URLs
- ✅ Use trending YouTube videos
- ✅ AI-powered highlight detection
- ✅ Automatic reel generation
- ✅ Download generated reels
- ✅ Upload to social media (with credentials)

## Troubleshooting
- **FFmpeg not found**: Download and install FFmpeg, add to PATH
- **API errors**: Check your OpenRouter API key in `.env`
- **Upload errors**: Configure social media credentials in `config/secrets.json`

---
**Need help?** Check the full README.md for detailed instructions! 