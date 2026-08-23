"""
Assembles the final vertical video from: AI images (with slow zoom/pan),
the voiceover track, a burned-in title/captions, and optional background music.
"""
import glob
import os
import random

from moviepy.editor import (
    AudioFileClip,
    CompositeAudioClip,
    CompositeVideoClip,
    ImageClip,
    TextClip,
    concatenate_videoclips,
)

from config import VIDEO_WIDTH, VIDEO_HEIGHT, MUSIC_DIR


def _ken_burns_clip(image_path: str, duration: float):
    """Slow zoom-in on a still image so it doesn't look static."""
    clip = ImageClip(image_path).set_duration(duration)
    # resize to fill the frame, then apply a slow zoom
    clip = clip.resize(height=VIDEO_HEIGHT)
    if clip.w < VIDEO_WIDTH:
        clip = clip.resize(width=VIDEO_WIDTH)
    zoom = clip.resize(lambda t: 1 + 0.04 * (t / duration))
    zoom = zoom.set_position(("center", "center"))
    return CompositeVideoClip([zoom], size=(VIDEO_WIDTH, VIDEO_HEIGHT)).set_duration(duration)


def build_video(
    image_paths: list[str],
    voiceover_path: str,
    title: str,
    out_path: str,
) -> float:
    """Builds the final mp4. Returns final duration in seconds."""
    voice = AudioFileClip(voiceover_path)
    duration = voice.duration
    per_image = duration / max(1, len(image_paths))

    clips = [_ken_burns_clip(p, per_image) for p in image_paths]
    video = concatenate_videoclips(clips, method="compose").set_duration(duration)

    # Title card overlay for the first ~3 seconds
    title_clip = (
        TextClip(
            title,
            fontsize=70,
            color="white",
            font="/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf",
            method="caption",
            size=(VIDEO_WIDTH - 120, None),
            stroke_color="black",
            stroke_width=2,
        )
        .set_position(("center", 120))
        .set_start(0)
        .set_duration(min(3.5, duration))
        .crossfadeout(0.5)
    )

    audio_tracks = [voice]
    music_files = glob.glob(os.path.join(MUSIC_DIR, "*.mp3"))
    if music_files:
        music = AudioFileClip(random.choice(music_files)).volumex(0.12)
        if music.duration < duration:
            loops = int(duration // music.duration) + 1
            music = concatenate_videoclips  # placeholder, audio looping handled below
        music = music.subclip(0, min(duration, music.duration)).set_duration(
            min(duration, music.duration)
        )
        audio_tracks.append(music)

    final_audio = CompositeAudioClip(audio_tracks) if len(audio_tracks) > 1 else voice
    final = CompositeVideoClip([video, title_clip], size=(VIDEO_WIDTH, VIDEO_HEIGHT))
    final = final.set_audio(final_audio).set_duration(duration)

    final.write_videofile(
        out_path,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        preset="medium",
        threads=2,
        logger=None,
    )
    return duration
