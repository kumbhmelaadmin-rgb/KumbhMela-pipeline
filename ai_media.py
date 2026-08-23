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

# A clear, natural-sounding free voice. Full list: `edge-tts --list-voices`
TTS_VOICE = "en-US-AriaNeural"


_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Referer": "https://github.com/kumbhmela-pipeline",
}


def fetch_ai_image(prompt: str, out_path: str, seed: int | None = None) -> None:
    """Download one AI-generated image for the given prompt (free, no API key)."""
    encoded = urllib.parse.quote(prompt)
    url = POLLINATIONS_IMAGE_URL.format(prompt=encoded)
    url += f"?width={VIDEO_WIDTH}&height={VIDEO_HEIGHT}&nologo=true"
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
