from moviepy.editor import VideoFileClip
import os

def extract_audio(video_path, output_dir="input/audio"):
    os.makedirs(output_dir, exist_ok=True)
    clip = VideoFileClip(video_path)
    audio_path = os.path.join(output_dir, os.path.basename(video_path).replace(".mp4", ".wav"))
    clip.audio.write_audiofile(audio_path, verbose=False, logger=None)
    return audio_path