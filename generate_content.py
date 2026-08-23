"""
STAGE 1 - runs on a schedule (see .github/workflows/generate.yml).
Picks a topic, writes a script, generates images + voiceover, builds the
video, commits it to /pending, and sends it to you on Telegram for approval.
"""
import json
import os
import random
import subprocess
import sys
import time
import uuid

from ai_media import fetch_ai_image, generate_voiceover
from ai_text import generate_image_prompts, pick_topic_and_write_script
from config import PENDING_DIR, SKIP_PROBABILITY
from telegram_utils import send_video_for_approval
from video_builder import build_video


def git_commit_and_push(paths: list[str], message: str):
    subprocess.run(["git", "config", "user.email", "bot@kumbhmela-pipeline"], check=True)
    subprocess.run(["git", "config", "user.name", "Kumbh Mela Content Bot"], check=True)
    subprocess.run(["git", "add", *paths], check=True)
    subprocess.run(["git", "commit", "-m", message], check=True)
    subprocess.run(["git", "push"], check=True)


def main():
    if random.random() < SKIP_PROBABILITY:
        print("Randomly skipping this run to vary posting frequency.")
        return

    from config import TOPIC_SEEDS

    print("Picking topic + writing script...")
    content = pick_topic_and_write_script(TOPIC_SEEDS)
    print(json.dumps(content, indent=2))

    job_id = f"{time.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"
    job_dir = os.path.join(PENDING_DIR, job_id)
    os.makedirs(job_dir, exist_ok=True)

    print("Generating AI image prompts...")
    image_prompts = generate_image_prompts(content["angle"], n=4)
    image_paths = []
    for i, p in enumerate(image_prompts):
        path = os.path.join(job_dir, f"img{i}.jpg")
        fetch_ai_image(p, path, seed=random.randint(1, 999999))
        image_paths.append(path)

    print("Generating voiceover...")
    audio_path = os.path.join(job_dir, "voice.mp3")
    generate_voiceover(content["script"], audio_path)

    print("Building video...")
    video_path = os.path.join(job_dir, "video.mp4")
    duration = build_video(image_paths, audio_path, content["title"], video_path)

    caption = content["title"] + "\n\n" + content["script"] + "\n\n" + " ".join(content["hashtags"])
    meta = {
        "job_id": job_id,
        "title": content["title"],
        "script": content["script"],
        "caption": caption,
        "duration_sec": round(duration, 1),
        "video_path": video_path,
        "status": "pending",
    }
    meta_path = os.path.join(job_dir, "meta.json")
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)

    print("Committing pending job to repo...")
    git_commit_and_push([job_dir], f"New pending video: {job_id}")

    print("Sending to Telegram for approval...")
    send_video_for_approval(video_path, caption, job_id)
    print("Done. Awaiting your approval in Telegram.")


if __name__ == "__main__":
    sys.exit(main())
