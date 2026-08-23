"""
Script writing. Tries free AI text generation (Pollinations) first for
variety; if that API is unavailable or its free-tier terms change again
(it has changed more than once), it silently falls back to a local
generator built from the curated TOPIC_FACTS bank in config.py. This way
the pipeline never breaks and never costs anything, regardless of what a
third-party free API does.
"""
import json
import random
import urllib.error
import urllib.parse
import urllib.request

from config import HASHTAG_BANK, TOPIC_FACTS

POLLINATIONS_TEXT_URL = "https://text.pollinations.ai/"

_HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Referer": "https://github.com/kumbhmela-pipeline",
    "Accept": "application/json",
}


def _call_pollinations(prompt: str, system: str = "") -> str:
    """POST to Pollinations' free text API. Raises on any failure - caller must handle."""
    payload = {
        "messages": ([{"role": "system", "content": system}] if system else [])
        + [{"role": "user", "content": prompt}],
        # No "model" key: some named models (e.g. "openai") now bill against
        # a paid pollen balance even for anonymous callers. Omitting it lets
        # Pollinations route to whatever is currently free.
    }
    req = urllib.request.Request(
        POLLINATIONS_TEXT_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers=_HEADERS,
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read().decode("utf-8", errors="ignore")
    try:
        data = json.loads(raw)
        if isinstance(data, dict) and "choices" in data:
            return data["choices"][0]["message"]["content"].strip()
        if isinstance(data, str):
            return data.strip()
    except json.JSONDecodeError:
        pass
    return raw.strip()


def _ai_pick_topic_and_write_script(topic_seeds: list[str]) -> dict:
    seed = random.choice(topic_seeds)
    system = (
        "You are a social media scriptwriter for an Instagram/Facebook page "
        "about Kumbh Mela (the Hindu pilgrimage festival). You write short, "
        "engaging, factually careful video scripts for a general global "
        "audience. Tone: fascinating, respectful, energetic. Keep facts "
        "accurate; if unsure, keep claims general."
    )
    prompt = f"""
Seed theme: "{seed}"

1. Narrow the seed into ONE specific, interesting angle.
2. Write a video voiceover script for that angle, 40-160 words, hook in the
   first line, plain spoken sentences (read aloud by text-to-speech), no
   emojis, no stage directions.
3. Suggest 6-8 relevant Instagram hashtags.
4. Suggest a short on-screen title (under 8 words).

Respond ONLY as strict JSON with keys: angle, title, script, hashtags (array).
"""
    raw = _call_pollinations(prompt, system=system)
    start, end = raw.find("{"), raw.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("AI response did not contain JSON")
    data = json.loads(raw[start : end + 1])
    required = {"angle", "title", "script", "hashtags"}
    if not required.issubset(data):
        raise ValueError("AI response missing required fields")
    data["seed"] = seed
    return data


def _local_pick_topic_and_write_script(topic_seeds: list[str]) -> dict:
    """Deterministic-but-varied fallback: no external calls, always works."""
    seed = random.choice(topic_seeds)
    facts = list(TOPIC_FACTS.get(seed, [f"Here's something worth knowing about {seed}."]))
    random.shuffle(facts)

    hooks = [
        "Here's something most people don't know about Kumbh Mela.",
        "This is one of the most fascinating facts about Kumbh Mela.",
        "You've probably never heard this about Kumbh Mela.",
        "Let's talk about something incredible from Kumbh Mela.",
    ]
    closers = [
        "That's the story of Kumbh Mela - faith, history, and scale like nowhere else on Earth.",
        "It's part of why Kumbh Mela remains one of the most extraordinary gatherings in human history.",
        "Follow along as we explore more of what makes Kumbh Mela so remarkable.",
    ]

    script = " ".join([random.choice(hooks), *facts[:3], random.choice(closers)])
    title = seed[:1].upper() + seed[1:]
    if len(title) > 55:
        title = title[:52] + "..."

    tags = random.sample(HASHTAG_BANK, k=min(6, len(HASHTAG_BANK)))
    return {
        "seed": seed,
        "angle": seed,
        "title": title,
        "script": script,
        "hashtags": tags,
    }


def pick_topic_and_write_script(topic_seeds: list[str]) -> dict:
    """
    Tries the free AI first for extra variety; falls back to a local,
    always-available generator if the AI call fails for any reason
    (network issue, API terms change, rate limit, malformed response, etc).
    """
    try:
        data = _ai_pick_topic_and_write_script(topic_seeds)
        print("Used AI-generated script.")
    except Exception as e:
        print(f"AI text generation unavailable ({e}); using local fallback script.")
        data = _local_pick_topic_and_write_script(topic_seeds)

    word_count = len(data["script"].split())
    data["suggested_duration_sec"] = max(15, min(65, round(word_count / 2.3)))
    return data


def generate_image_prompts(angle: str, n: int = 4) -> list[str]:
    """Ask the AI for n distinct visual scene descriptions; falls back to
    generic but relevant prompts if the AI call fails."""
    system = (
        "You write concise, vivid image-generation prompts for an AI image "
        "model. Describe realistic, respectful, culturally accurate scenes "
        "related to Kumbh Mela. No text/watermarks in the described image."
    )
    prompt = (
        f'Give {n} distinct visual scene descriptions (1 sentence each) that could '
        f'illustrate this video topic: "{angle}". '
        f'Respond ONLY as a JSON array of {n} strings.'
    )
    try:
        raw = _call_pollinations(prompt, system=system)
        start, end = raw.find("["), raw.rfind("]")
        prompts = json.loads(raw[start : end + 1])
        if isinstance(prompts, list) and prompts:
            return prompts[:n]
        raise ValueError("empty/invalid prompt list")
    except Exception as e:
        print(f"AI image-prompt generation unavailable ({e}); using generic prompts.")
        generic = [
            f"A wide, vivid photograph capturing {angle}, golden hour lighting, documentary style",
            "Pilgrims gathered on the banks of a sacred river at Kumbh Mela, misty morning light",
            "Colorful tents and flags of a Kumbh Mela monastic camp at dusk",
            "A close-up portrait-style scene of a devotee in prayer at Kumbh Mela, respectful and serene",
        ]
        return generic[:n]
