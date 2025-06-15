from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

def create_reel(video_path, scenes, output_path="output/reels/reel.mp4"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    video_clip = VideoFileClip(video_path)
    clips = []

    for i, (start, end) in enumerate(scenes):
        # Ensure start < end and within video bounds
        if start < 0:
            print(f"⚠️ Scene {i}: Start time < 0. Skipping.")
            continue
        if end > video_clip.duration:
            print(f"⚠️ Scene {i}: End time exceeds video length. Trimming...")
            end = video_clip.duration
        if start >= end:
            print(f"⚠️ Scene {i}: Invalid segment (start >= end). Skipping.")
            continue

        try:
            clip = video_clip.subclip(start, end)
            clips.append(clip)
        except Exception as e:
            print(f"❌ Failed to extract segment {start}-{end}: {e}")

    if not clips:
        raise ValueError("No valid segments found to generate reel.")

    final_clip = concatenate_videoclips(clips)
    final_clip = final_clip.subclip(0, min(30, final_clip.duration))  # Trim to 30s max
    final_clip.write_videofile(output_path, codec='libx264', verbose=False, logger=None)
    return output_path
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    clips = []
    video_clip = VideoFileClip(video_path)

    for start, end in scenes:
        try:
            clip = video_clip.subclip(start, min(end, video_clip.duration))
            clips.append(clip)
        except Exception as e:
            print(f"Error trimming segment {start}-{end}: {e}")

    if not clips:
        raise ValueError("No valid segments found to generate reel.")

    final_clip = concatenate_videoclips(clips)
    final_clip = final_clip.subclip(0, 30)  # Trim to 30 seconds
    final_clip.write_videofile(output_path, codec='libx264', verbose=False, logger=None)
    return output_path