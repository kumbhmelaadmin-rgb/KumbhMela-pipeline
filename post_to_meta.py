"""
Posts an approved video to Instagram (as a Reel) and Facebook (as a video post)
using the Meta Graph API. Requires a long-lived Page access token with
instagram_content_publish + pages_manage_posts permissions.

NOTE: The video must be reachable at a public HTTPS URL for Instagram's
Graph API (it fetches the video itself, you can't just upload bytes for Reels).
This script therefore expects the video to already be hosted somewhere public
(see README - we host it via a temporary public GitHub raw URL from the repo,
or you can point PUBLIC_VIDEO_URL_BASE at your own storage).
"""
import json
import os
import time
import urllib.parse
import urllib.request

GRAPH_VERSION = "v20.0"
PAGE_ACCESS_TOKEN = os.environ["META_PAGE_ACCESS_TOKEN"]
FACEBOOK_PAGE_ID = os.environ["META_FACEBOOK_PAGE_ID"]
IG_BUSINESS_ID = os.environ["META_IG_BUSINESS_ID"]


def _call(url: str, data: dict | None = None, method: str = "GET"):
    if method == "GET":
        if data:
            url = f"{url}?{urllib.parse.urlencode(data)}"
        req = urllib.request.Request(url, method="GET")
    else:
        body = urllib.parse.urlencode(data or {}).encode()
        req = urllib.request.Request(url, data=body, method=method)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read())


def post_facebook_video(public_video_url: str, caption: str):
    url = f"https://graph-video.facebook.com/{GRAPH_VERSION}/{FACEBOOK_PAGE_ID}/videos"
    return _call(
        url,
        data={
            "file_url": public_video_url,
            "description": caption,
            "access_token": PAGE_ACCESS_TOKEN,
        },
        method="POST",
    )


def post_instagram_reel(public_video_url: str, caption: str):
    # Step 1: create a media container
    create_url = f"https://graph.facebook.com/{GRAPH_VERSION}/{IG_BUSINESS_ID}/media"
    container = _call(
        create_url,
        data={
            "media_type": "REELS",
            "video_url": public_video_url,
            "caption": caption,
            "access_token": PAGE_ACCESS_TOKEN,
        },
        method="POST",
    )
    creation_id = container["id"]

    # Step 2: poll until Instagram finishes processing the video
    status_url = f"https://graph.facebook.com/{GRAPH_VERSION}/{creation_id}"
    for _ in range(30):
        status = _call(
            status_url,
            data={"fields": "status_code", "access_token": PAGE_ACCESS_TOKEN},
            method="GET",
        )
        if status.get("status_code") == "FINISHED":
            break
        time.sleep(10)

    # Step 3: publish
    publish_url = f"https://graph.facebook.com/{GRAPH_VERSION}/{IG_BUSINESS_ID}/media_publish"
    return _call(
        publish_url,
        data={"creation_id": creation_id, "access_token": PAGE_ACCESS_TOKEN},
        method="POST",
    )
