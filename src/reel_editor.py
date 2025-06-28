from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip
import os
import emoji

from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})

def create_reel(video_path, segments, caption=None, output_path="output/reels/reel.mp4"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    video_clip = VideoFileClip(video_path)
    clips = []

    # Trim and collect valid segments
    for start, end in segments:
        if start < 0 or end > video_clip.duration or start >= end:
            continue
        try:
            clip = video_clip.subclip(start, end)
            clips.append(clip)
        except Exception as e:
            print(f"❌ Failed to extract segment {start}-{end}: {e}")

    if not clips:
        raise ValueError("No valid segments found to generate reel.")

    # Concatenate all selected parts
    final_clip = concatenate_videoclips(clips)

    # Trim to exactly 30 seconds
    final_clip = final_clip.subclip(0, min(30, final_clip.duration))

    caption = emoji.emojize(caption, language='alias')  # Converts :fire: to 🔥 etc.

    # Add caption if provided
    if caption:
        txt_clip = TextClip(
            caption,
            fontsize=40,
            color='white',
            bg_color='black',
            stroke_color='black',
            stroke_width=2,
            size=(final_clip.w, 100)
        )
        # txt_clip = TextClip(
        #     caption,
        #     fontsize=60,
        #     color='yellow',
        #     font='Arial-Bold',
        #     bg_color='rgba(0,0,0,0.5)',
        #     stroke_color='black',
        #     stroke_width=3
        # ).set_position(('center', 'bottom'))

        txt_clip = txt_clip.set_position(('center', 'bottom')).set_duration(final_clip.duration)
        final_clip = CompositeVideoClip([final_clip, txt_clip])

    # Write final reel
    final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac', verbose=False, logger=None)
    return output_path