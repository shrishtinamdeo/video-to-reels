import whisper_timestamped as whisper
import os

def transcribe_with_timestamps(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result['segments']