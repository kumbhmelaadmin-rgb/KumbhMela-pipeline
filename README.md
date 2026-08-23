# Kumbh Mela Auto-Content Pipeline

Free, automated Instagram + Facebook video pipeline with a human approval step.

## How it works
1. **`generate.yml`** runs on a schedule (twice daily, ~15% chance of skipping
   a run so frequency varies). It picks a topic, writes a script (free AI text),
   makes AI images + a voiceover (free), builds a 15s-65s vertical video, and
   sends it to you on **Telegram** with Approve/Reject buttons.
2. You tap a button on your phone.
3. **`check_approval.yml`** runs every 15 min, sees your tap, and if approved,
   posts the video to your Instagram (as a Reel) and Facebook Page automatically.

Nothing posts without your tap.

---

## One-time setup (do this once, ~30-45 min total)

### 1. Create the GitHub repo
Upload everything in this folder to a **new GitHub repository**. It must be
**public** (the free approach uses the raw GitHub URL of the video file so
Instagram's API can fetch it — a private repo's files aren't publicly fetchable).
If you don't want a public repo, see the note at the bottom about alternative hosting.

### 2. Create your Telegram approval bot (5 min, free)
1. In Telegram, message **@BotFather** → `/newbot` → follow prompts → copy the
   **bot token** it gives you.
2. Message **@userinfobot** → it replies with your numeric **chat ID** → copy it.
3. Send your new bot any message first (e.g. "hi") so it's allowed to message you back.

### 3. Set up Meta (Facebook + Instagram) access — the longer part
1. Make sure your Instagram account is a **Business** account, linked to a
   **Facebook Page** you manage (Instagram app → Settings → Account type → Switch
   to Professional → Business, then link/create the connected Facebook Page).
2. Go to **developers.facebook.com** → My Apps → Create App → choose "Other" →
   "Business" type.
3. In the app, add the **Facebook Login** and **Instagram Graph API** products.
4. Use the **Graph API Explorer** (developers.facebook.com/tools/explorer):
   - Select your app, select your Page, and request these permissions:
     `pages_manage_posts`, `pages_read_engagement`, `instagram_basic`,
     `instagram_content_publish`.
   - Generate a **User Access Token**, then exchange it for a **long-lived Page
     Access Token** (Meta's docs page "Long-Lived Access Tokens" — this is the
     one non-automatable step; Meta tokens need periodic renewal, roughly every
     60 days unless you set up a System User token, which doesn't expire).
5. Get your **Facebook Page ID** (Page → About → Page ID) and your **Instagram
   Business Account ID** (Graph API Explorer: `GET /me/accounts` → find your
   page → `GET /{page-id}?fields=instagram_business_account`).

### 4. Add secrets to GitHub
In your repo: **Settings → Secrets and variables → Actions → New repository secret**.
Add all of these:

| Secret name | Value |
|---|---|
| `TELEGRAM_BOT_TOKEN` | from BotFather |
| `TELEGRAM_CHAT_ID` | from userinfobot |
| `META_PAGE_ACCESS_TOKEN` | long-lived Page token from step 3 |
| `META_FACEBOOK_PAGE_ID` | your Page ID |
| `META_IG_BUSINESS_ID` | your Instagram Business Account ID |

### 5. Test it
Go to the repo's **Actions** tab → "Generate Kumbh Mela Video" → **Run workflow**
(manual trigger, don't need to wait for the schedule). Check Telegram for the
video a couple minutes later. Tap Approve, then manually run "Check Approvals
& Publish" (or wait up to 15 min) and check your Page/Instagram.

---

## Adjusting things later
- **Topics**: edit the `TOPIC_SEEDS` list in `config.py`.
- **Posting frequency**: edit the `cron` lines in `.github/workflows/generate.yml`
  (add more times for more videos/day) and `SKIP_PROBABILITY` in `config.py`.
- **Voice**: change `TTS_VOICE` in `ai_media.py` (run `edge-tts --list-voices`
  locally to see options, including Hindi voices like `hi-IN-MadhurNeural`).
- **Background music**: drop royalty-free `.mp3` files (e.g. from Pixabay Music,
  YouTube Audio Library) into `assets/music/` and commit them — the video
  builder will pick one at random and mix it under the voiceover.

## Known limitations to be aware of
- Meta's Page access tokens expire periodically — you'll need to regenerate
  and update the `META_PAGE_ACCESS_TOKEN` secret roughly every 60 days unless
  you set up a non-expiring System User token (more setup, worth it long-term).
- Pollinations.ai's free endpoints are shared and unauthenticated, so quality
  and uptime can vary run to run — that's the trade-off for zero cost.
- If you'd rather not make the repo public, swap `public_video_url()` in
  `check_and_publish.py` to point at any free public file host you upload the
  video to instead (e.g. a free Cloudflare R2/Backblaze bucket).
- I've written and reviewed this code carefully but haven't been able to run
  it end-to-end against live Meta/Telegram accounts myself — budget your first
  test run for troubleshooting a few small config issues, which is normal.
