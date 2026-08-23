"""
Free, no-API-key text generation using the Pollinations.ai text endpoint.
Used to pick a specific angle on a topic and write a short video script.
"""
import json
import random
import urllib.error
import urllib.parse
import urllib.request

POLLINATIONS_TEXT_URL = "https://text.pollinations.ai/"


def _call_pollinations(prompt: str, system: str = "") -> str:
    """POST a chat-style request to Pollinations' free text API and return plain text."""
    payload = {
        "messages": (
            [{"role": "system", "content": system}] if system else []
        )
        + [{"role": "user", "content": prompt}],
        "model": "openai",  # free routed model on Pollinations
    }
    req = urllib.request.Request(
        POLLINATIONS_TEXT_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
            ),
            "Referer": "https://github.com/kumbhmela-pipeline",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8", errors="ignore")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")
        raise RuntimeError(
            f"Pollinations text API returned {e.code}: {body[:500]}"
        ) from e
    # Pollinations sometimes returns plain text, sometimes JSON-wrapped text
    try:
        data = json.loads(raw)
        if isinstance(data, dict) and "choices" in data:
            return data["choices"][0]["message"]["content"].strip()
        if isinstance(data, str):
            return data.strip()
    except json.JSONDecodeError:
        pass
    return raw.strip()


def pick_topic_and_write_script(topic_seeds: list[str]) -> dict:
    """
    Asks the free AI to:
      1. pick ONE seed topic
      2. narrow it to a specific, fresh angle
      3. write a punchy short-video script (15-60s spoken length)
    Returns dict: {seed, angle, title, script, hashtags, suggested_duration_sec}
    """
    seed = random.choice(topic_seeds)

    system = (
        "You are a social media scriptwriter for an Instagram/Facebook page "
        "about Kumbh Mela (the Hindu pilgrimage festival). You write short, "
        "engaging, factually careful video scripts for a general global "
        "audience. Tone: fascinating, respectful, energetic — never dry or "
        "textbook-like. Keep facts accurate; if unsure, keep claims general."
    )
    prompt = f"""
Seed theme: "{seed}"

Do this:
1. Narrow the seed into ONE specific, interesting angle (a fact, story, or question)
   that hasn't been overused on social media.
2. Write a video voiceover script for that angle. Length: choose whatever best
   fits the topic, between 15 and 60 seconds of spoken audio (roughly 40-160 words).
   Hook in the first line. Simple spoken sentences (this will be read by
   text-to-speech). No stage directions, no emojis in the script text itself.
3. Suggest 6-8 relevant Instagram hashtags (no explanation, just the tags).
4. Suggest a short on-screen title (under 8 words).

Respond ONLY as strict JSON with keys:
angle, title, script, hashtags (array of strings, each starting with #)
"""
    raw = _call_pollinations(prompt, system=system)

    # Try to extract JSON even if the model wrapped it in extra text
    start = raw.find("{")
    end = raw.rfind("}")
    data = json.loads(raw[start : end + 1])

    data["seed"] = seed
    word_count = len(data["script"].split())
    # rough spoken pace ~2.3 words/sec -> estimate duration
    data["suggested_duration_sec"] = max(15, min(65, round(word_count / 2.3)))
    return data


def generate_image_prompts(angle: str, n: int = 4) -> list[str]:
    """Ask the AI for n distinct visual scene descriptions to illustrate the script."""
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
    raw = _call_pollinations(prompt, system=system)
    start = raw.find("[")
    end = raw.rfind("]")
    prompts = json.loads(raw[start : end + 1])
    return prompts[:n]
