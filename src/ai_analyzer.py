from scenedetect import detect, ContentDetector
import librosa

# Scene detection
def detect_scenes(video_path):
    try:
        scene_list = detect(video_path, ContentDetector())
        scenes = [(float(scene[0].get_seconds()), float(scene[1].get_seconds())) for scene in scene_list]
        return scenes[:5]  # Top 5 scenes
    except Exception as e:
        print(f"⚠️ Scene detection failed: {e}")
        return []

# Audio peak detection
def find_audio_peaks(audio_path):
    y, sr = librosa.load(audio_path)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    peaks = librosa.util.peak_pick(onset_env, pre_max=20, post_max=20, delta=0.4, wait=10)
    timestamps = [float(librosa.frames_to_time(p, sr=sr)) for p in peaks]
    return timestamps