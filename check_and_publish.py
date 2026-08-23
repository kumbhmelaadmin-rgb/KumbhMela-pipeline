"""
STAGE 2 - runs frequently (e.g. every 10-15 min, see check_approval.yml).
Checks Telegram for your Approve/Reject taps. On approve, publishes to
Instagram + Facebook. On reject, deletes the pending job.

IMPORTANT: Instagram's Graph API fetches the video from a public HTTPS URL
rather than accepting an upload. This script uses the raw GitHub URL of the
committed video file, which means YOUR REPO MUST BE PUBLIC (or you must
point PUBLIC_VIDEO_URL_BASE at your own public hosting - see README).
"""
import json
import os
import shutil
import subprocess
import sys

from config import PENDING_DIR, POSTED_DIR
from post_to_meta import post_facebook_video, post_instagram_reel
from telegram_utils import get_button_presses

GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "")  # e.g. "yourname/kumbhmela-pipeline"
GITHUB_REF_NAME = os.environ.get("GITHUB_REF_NAME", "main")
OFFSET_FILE = ".telegram_offset"


def public_video_url(video_path: str) -> str:
    return f"https://raw.githubusercontent.com/{GITHUB_REPOSITORY}/{GITHUB_REF_NAME}/{video_path}"


def git_commit_and_push(message: str):
    subprocess.run(["git", "config", "user.email", "bot@kumbhmela-pipeline"], check=True)
    subprocess.run(["git", "config", "user.name", "Kumbh Mela Content Bot"], check=True)
    subprocess.run(["git", "add", "-A"], check=True)
    result = subprocess.run(["git", "commit", "-m", message])
    if result.returncode == 0:
        subprocess.run(["git", "push"], check=True)


def main():
    offset = 0
    if os.path.exists(OFFSET_FILE):
        offset = int(open(OFFSET_FILE).read().strip() or 0)

    presses, new_offset = get_button_presses(offset)
    with open(OFFSET_FILE, "w") as f:
        f.write(str(new_offset))

    if not presses:
        print("No new approvals/rejections.")
        return

    for job_id, decision, _ in presses:
        job_dir = os.path.join(PENDING_DIR, job_id)
        meta_path = os.path.join(job_dir, "meta.json")
        if not os.path.exists(meta_path):
            print(f"Job {job_id} not found (already processed?), skipping.")
            continue
        with open(meta_path) as f:
            meta = json.load(f)

        if decision == "approve":
            print(f"Approved: {job_id} - publishing...")
            url = public_video_url(meta["video_path"])
            try:
                fb_result = post_facebook_video(url, meta["caption"])
                print("Facebook:", fb_result)
            except Exception as e:
                print("Facebook post FAILED:", e)
            try:
                ig_result = post_instagram_reel(url, meta["caption"])
                print("Instagram:", ig_result)
            except Exception as e:
                print("Instagram post FAILED:", e)

            dest = os.path.join(POSTED_DIR, job_id)
            shutil.move(job_dir, dest)
            meta["status"] = "posted"
            with open(os.path.join(dest, "meta.json"), "w") as f:
                json.dump(meta, f, indent=2)

        elif decision == "reject":
            print(f"Rejected: {job_id} - deleting.")
            shutil.rmtree(job_dir, ignore_errors=True)

    git_commit_and_push("Process Telegram approvals")


if __name__ == "__main__":
    sys.exit(main())
