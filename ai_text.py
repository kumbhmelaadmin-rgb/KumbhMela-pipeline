"""
Script writing, in Hindi. Tries free AI text generation (Pollinations)
first for variety; falls back to a local generator built from the curated
TOPIC_FACTS bank in config.py if that API is unavailable (it has changed
terms more than once). This way the pipeline never breaks and never costs
anything, regardless of what a third-party free API does.
"""
import json
import random
import urllib.error
import urllib.parse
import urllib.request

from config import CLOSERS_HI, HASHTAG_BANK, HOOKS_HI, TOPIC_FACTS, TOPIC_TITLES_HI

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
        "आप कुंभ मेला (हिंदू तीर्थ पर्व) के बारे में एक इंस्टाग्राम/फेसबुक पेज के लिए "
        "स्क्रिप्ट लिखने वाले एक कुशल हिंदी कंटेंट राइटर हैं। आप छोटी, आकर्षक, तथ्यात्मक "
        "रूप से सही वीडियो स्क्रिप्ट पूरी तरह शुद्ध हिंदी (देवनागरी) में लिखते हैं। लहजा: "
        "रोचक, सम्मानजनक, ऊर्जावान। तथ्यों को सही रखें; अनिश्चित होने पर सामान्य बात कहें।"
    )
    prompt = f"""
विषय: "{seed}"

यह करें:
1. इस विषय का कोई एक खास, दिलचस्प पहलू चुनें।
2. उस पहलू पर एक वीडियो वॉइसओवर स्क्रिप्ट लिखें, पूरी तरह हिंदी (देवनागरी) में, 40-160 शब्द,
   पहली पंक्ति में ध्यान खींचने वाली बात, सरल बोलचाल के वाक्य (टेक्स्ट-टू-स्पीच द्वारा पढ़े जाएंगे),
   कोई इमोजी या निर्देश नहीं।
3. 6-8 प्रासंगिक इंस्टाग्राम हैशटैग सुझाएं (हिंदी और अंग्रेज़ी मिश्रित ठीक है)।
4. एक छोटा ऑन-स्क्रीन शीर्षक सुझाएं (8 शब्दों से कम, हिंदी में)।

केवल सख्त JSON के रूप में जवाब दें, इन keys के साथ: angle, title, script, hashtags (array)।
angle को अंग्रेज़ी में संक्षेप में रखें, बाकी सब हिंदी में।
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
    """Deterministic-but-varied Hindi fallback: no external calls, always works."""
    seed = random.choice(topic_seeds)
    facts = list(TOPIC_FACTS.get(seed, [f"{seed} के बारे में एक खास बात।"]))
    random.shuffle(facts)

    script = " ".join([random.choice(HOOKS_HI), *facts[:3], random.choice(CLOSERS_HI)])
    title = TOPIC_TITLES_HI.get(seed, seed)

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
    always-available Hindi generator if the AI call fails for any reason
    (network issue, API terms change, rate limit, malformed response, etc).
    """
    try:
        data = _ai_pick_topic_and_write_script(topic_seeds)
        print("Used AI-generated Hindi script.")
    except Exception as e:
        print(f"AI text generation unavailable ({e}); using local Hindi fallback script.")
        data = _local_pick_topic_and_write_script(topic_seeds)

    # Hindi is spoken a bit slower per word on average than English TTS;
    # ~2.0 words/sec is a safer estimate than the ~2.3 used for English.
    word_count = len(data["script"].split())
    data["suggested_duration_sec"] = max(15, min(65, round(word_count / 2.0)))
    return data


def generate_image_prompts(angle: str, n: int = 4) -> list[str]:
    """Ask the AI for n distinct visual scene descriptions (kept in English -
    image models respond better to English prompts); falls back to generic
    but relevant prompts if the AI call fails."""
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
