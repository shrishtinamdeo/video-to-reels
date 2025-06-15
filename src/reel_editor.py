from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

def create_reel(video_path, segments, output_path="output/reels/reel.mp4"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    video_clip = VideoFileClip(video_path)
    clips = []

    for seg in segments:
        start = float(seg["start"])
        end = float(seg["end"])

        if start < 0 or end > video_clip.duration or start >= end:
            continue

        try:
            clip = video_clip.subclip(start, end)
            clips.append(clip)
        except Exception as e:
            print(f"❌ Failed to extract segment {start}-{end}: {e}")

    if not clips:
        raise ValueError("No valid segments found to generate reel.")

    final_clip = concatenate_videoclips(clips)
    final_clip = final_clip.subclip(0, min(30, final_clip.duration))
    final_clip.write_videofile(output_path, codec='libx264', verbose=False, logger=None)
    return output_path