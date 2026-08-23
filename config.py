"""
Central config for the Kumbh Mela content pipeline.
Edit TOPIC_SEEDS any time to steer what the AI talks about.
"""

# Seed themes. The script-writer AI picks one at random each run and
# is told to find a FRESH, SPECIFIC angle within it (so you don't get
# the same video twice even if the same seed comes up again).
TOPIC_SEEDS = [
    "the history and origin of Kumbh Mela",
    "the mythology of Samudra Manthan and how it connects to Kumbh Mela",
    "the four Kumbh Mela locations: Prayagraj, Haridwar, Ujjain, Nashik",
    "Naga Sadhus - who they are and their way of life",
    "the Akharas (monastic orders) of Kumbh Mela",
    "Shahi Snan (the royal bath) - what it is and why it matters",
    "how Kumbh Mela became a UNESCO Intangible Cultural Heritage",
    "the scale of Kumbh Mela - crowd numbers, logistics, temporary city facts",
    "spiritual significance of bathing in the Ganga during Kumbh",
    "lesser-known rituals and traditions at Kumbh Mela",
    "food and langar (community kitchen) culture at Kumbh Mela",
    "how astrology (planetary positions) decides the Kumbh Mela dates",
    "a short devotional/inspirational message tied to Kumbh Mela values",
    "safety and travel tips for pilgrims visiting Kumbh Mela",
    "a myth-busting fact about Kumbh Mela most people get wrong",
]

# Video settings
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920  # vertical, for Reels/Shorts-style posts
MIN_DURATION_SEC = 15
MAX_DURATION_SEC = 65

# Posting cadence: generate.yml can run multiple times a day (see workflow).
# This flag lets the script itself randomly SKIP a run so frequency isn't
# perfectly regular (e.g. some days 1 video, some days 2).
SKIP_PROBABILITY = 0.15  # 15% chance a given scheduled run produces nothing

# Where generated (not-yet-approved) videos live inside the repo
PENDING_DIR = "pending"
POSTED_DIR = "posted"

# Optional local royalty-free background music (put .mp3 files here yourself;
# leave empty to post with voiceover only, no background music)
MUSIC_DIR = "assets/music"
