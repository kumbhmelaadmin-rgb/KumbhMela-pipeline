"""
Free AI image generation (Pollinations image API, no key) and
free text-to-speech voiceover generation (edge-tts).
"""
import asyncio
import urllib.parse
import urllib.request

import edge_tts

from config import VIDEO_WIDTH, VIDEO_HEIGHT

POLLINATIONS_IMAGE_URL = "https://image.pollinations.ai/prompt/{prompt}"

# A clear, natural-sounding free Hindi male voice.
# Full list: `edge-tts --list-voices` (other good options: hi-IN-MadhurNeural)
TTS_VOICE = "hi-IN-MadhurNeural"


_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Referer": "https://github.com/kumbhmela-pipeline",
}

# Fetch images at a higher resolution than the final video canvas, then
# downscale during video assembly - this supersampling makes the final
# result noticeably sharper/HD-looking versus fetching at exact output size.
IMAGE_FETCH_WIDTH = int(VIDEO_WIDTH * 1.5)
IMAGE_FETCH_HEIGHT = int(VIDEO_HEIGHT * 1.5)


def fetch_ai_image(prompt: str, out_path: str, seed: int | None = None) -> None:
    """Download one AI-generated image for the given prompt (free, no API key)."""
    quality_suffix = ", highly detailed, sharp focus, professional photography, 4k"
    encoded = urllib.parse.quote(prompt + quality_suffix)
    url = POLLINATIONS_IMAGE_URL.format(prompt=encoded)
    url += f"?width={IMAGE_FETCH_WIDTH}&height={IMAGE_FETCH_HEIGHT}&nologo=true&enhance=true"
    if seed is not None:
        url += f"&seed={seed}"
    req = urllib.request.Request(url, headers=_HEADERS)
    with urllib.request.urlopen(req, timeout=90) as resp, open(out_path, "wb") as f:
        f.write(resp.read())


async def _tts(text: str, out_path: str) -> None:
    communicate = edge_tts.Communicate(text, TTS_VOICE)
    await communicate.save(out_path)


def generate_voiceover(script_text: str, out_path: str) -> None:
    """Free TTS voiceover via Microsoft Edge's TTS engine (edge-tts package)."""
    asyncio.run(_tts(script_text, out_path))
