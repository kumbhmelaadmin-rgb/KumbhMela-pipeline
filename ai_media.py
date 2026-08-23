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


def fetch_ai_image(prompt: str, out_path: str, seed: int | None = None) -> None:
    """Download one AI-generated image for the given prompt (free, no API key)."""
    encoded = urllib.parse.quote(prompt)
    url = POLLINATIONS_IMAGE_URL.format(prompt=encoded)
    url += f"?width={VIDEO_WIDTH}&height={VIDEO_HEIGHT}&nologo=true"
    if seed is not None:
        url += f"&seed={seed}"
    urllib.request.urlretrieve(url, out_path)


async def _tts(text: str, out_path: str) -> None:
    communicate = edge_tts.Communicate(text, TTS_VOICE)
    await communicate.save(out_path)


def generate_voiceover(script_text: str, out_path: str) -> None:
    """Free TTS voiceover via Microsoft Edge's TTS engine (edge-tts package)."""
    asyncio.run(_tts(script_text, out_path))
