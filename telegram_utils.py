"""
Telegram is used purely as your free 'approve / reject' inbox.
Create a bot via @BotFather (free), and get your own numeric chat ID by
messaging @userinfobot (free). Both go into GitHub Secrets - see README.
"""
import json
import os
import urllib.request

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"


def _post(method: str, fields: dict, files: dict | None = None):
    url = f"{API_BASE}/{method}"
    if not files:
        req = urllib.request.Request(
            url,
            data=json.dumps(fields).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read())
    else:
        # multipart upload (for video)
        import mimetypes
        import uuid

        boundary = uuid.uuid4().hex
        body = b""
        for key, value in fields.items():
            body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{key}\"\r\n\r\n{value}\r\n".encode()
        for key, path in files.items():
            ctype = mimetypes.guess_type(path)[0] or "application/octet-stream"
            with open(path, "rb") as f:
                content = f.read()
            body += (
                f'--{boundary}\r\nContent-Disposition: form-data; name="{key}"; '
                f'filename="{os.path.basename(path)}"\r\nContent-Type: {ctype}\r\n\r\n'
            ).encode() + content + b"\r\n"
        body += f"--{boundary}--\r\n".encode()
        req = urllib.request.Request(
            url, data=body, headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read())


def send_video_for_approval(video_path: str, caption: str, job_id: str):
    """Sends the generated video to you with Approve/Reject inline buttons."""
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "✅ Approve & Post", "callback_data": f"approve:{job_id}"},
                {"text": "❌ Reject", "callback_data": f"reject:{job_id}"},
            ]
        ]
    }
    fields = {
        "chat_id": CHAT_ID,
        "caption": caption[:1024],
        "reply_markup": json.dumps(keyboard),
    }
    return _post("sendVideo", fields, files={"video": video_path})


def get_button_presses(offset: int = 0):
    """Poll for any button taps since `offset`. Returns list of (job_id, decision, update_id)."""
    resp = _post("getUpdates", {"offset": offset, "timeout": 0})
    results = []
    max_update_id = offset - 1
    for update in resp.get("result", []):
        max_update_id = max(max_update_id, update["update_id"])
        cq = update.get("callback_query")
        if not cq:
            continue
        data = cq.get("data", "")
        if ":" not in data:
            continue
        decision, job_id = data.split(":", 1)
        results.append((job_id, decision, update["update_id"]))
        # acknowledge the button press so Telegram stops showing the spinner
        _post("answerCallbackQuery", {"callback_query_id": cq["id"]})
    return results, max_update_id + 1
