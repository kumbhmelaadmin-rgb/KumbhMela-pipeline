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

# Backup fact bank used to LOCALLY write a script if the free AI text API
# is unavailable or changes its terms again (keeps the pipeline 100% free
# and never dependent on a single third party staying free forever).
TOPIC_FACTS = {
    "the history and origin of Kumbh Mela": [
        "Kumbh Mela's roots trace back over a thousand years, linked to the legend of the gods and demons fighting over a pot of nectar of immortality.",
        "Drops of that nectar are believed to have fallen at four places on Earth - Prayagraj, Haridwar, Ujjain, and Nashik - which is why the festival rotates between them.",
        "Adi Shankaracharya, the 8th-century philosopher, is often credited with organizing the gatherings of monks into the structured festival we recognize today.",
    ],
    "the mythology of Samudra Manthan and how it connects to Kumbh Mela": [
        "The Samudra Manthan is the story of gods and demons churning the cosmic ocean together to obtain Amrita, the nectar of immortality.",
        "As the pot of nectar was carried away, drops are said to have spilled at four earthly locations - the very sites where Kumbh Mela is held today.",
        "This is why devotees believe bathing at these sites during Kumbh carries the same purifying power as that mythical nectar.",
    ],
    "the four Kumbh Mela locations: Prayagraj, Haridwar, Ujjain, Nashik": [
        "Kumbh Mela rotates between four sacred rivers: the Ganga at Prayagraj and Haridwar, the Shipra at Ujjain, and the Godavari at Nashik.",
        "Each location hosts the full Kumbh roughly once every 12 years, meaning any single site sees it only a handful of times in a lifetime.",
        "Prayagraj's Kumbh is considered the largest, held at the sacred Sangam - the confluence of the Ganga, Yamuna, and the mythical Saraswati river.",
    ],
    "Naga Sadhus - who they are and their way of life": [
        "Naga Sadhus are warrior-ascetics who renounce all worldly possessions, including clothing, as a mark of complete detachment from material life.",
        "Becoming a Naga Sadhu can take over a decade of rigorous training, meditation, and tests of endurance under a guru.",
        "They are famous for leading the Shahi Snan, the royal procession into the river, at every Kumbh Mela.",
    ],
    "the Akharas (monastic orders) of Kumbh Mela": [
        "Akharas are centuries-old monastic orders of Hindu ascetics, each with its own traditions, deities, and hierarchy.",
        "There are 13 major Akharas recognized today, some tracing their founding back to the 8th century.",
        "At Kumbh Mela, Akharas set up massive camps and lead the ceremonial processions in a strict, ancient order of precedence.",
    ],
    "Shahi Snan (the royal bath) - what it is and why it matters": [
        "Shahi Snan, or the 'royal bath,' is the most sacred ritual bathing event of Kumbh Mela, timed to precise astrological moments.",
        "Naga Sadhus and Akhara leaders bathe first in a grand procession, followed by millions of pilgrims believed to gain the same spiritual merit.",
        "The specific auspicious dates are calculated using planetary positions months or years in advance.",
    ],
    "how Kumbh Mela became a UNESCO Intangible Cultural Heritage": [
        "UNESCO added Kumbh Mela to its Representative List of the Intangible Cultural Heritage of Humanity in 2017.",
        "It was recognized for its scale, diversity of ritual practice, and its role in fostering a sense of universal brotherhood among pilgrims.",
        "UNESCO specifically noted the festival's peaceful coexistence of so many different monastic and devotional traditions in one place.",
    ],
    "the scale of Kumbh Mela - crowd numbers, logistics, temporary city facts": [
        "Kumbh Mela is considered the largest peaceful gathering of human beings on the planet, with past events drawing over 100 million visitors across the festival period.",
        "A temporary city is built from scratch for the event, complete with roads, bridges, hospitals, and its own police force.",
        "On the single biggest bathing day, tens of millions of people can gather at the riverbanks within just a few hours.",
    ],
    "spiritual significance of bathing in the Ganga during Kumbh": [
        "Bathing in the Ganga during Kumbh Mela is believed to wash away sins accumulated over many lifetimes.",
        "Pilgrims travel from across India and the world specifically to bathe at the exact astrologically auspicious moment.",
        "For many, it isn't just a ritual - it's considered a once-in-a-lifetime opportunity for spiritual liberation, or moksha.",
    ],
    "lesser-known rituals and traditions at Kumbh Mela": [
        "Beyond the famous royal baths, Kumbh Mela includes days of religious discourses, devotional singing, and philosophical debates among scholars.",
        "Many pilgrims perform Pind Daan, a ritual to honor deceased ancestors, during their visit.",
        "Some ascetics undertake extreme, decades-long vows during Kumbh - like never sitting down, or keeping an arm raised permanently - as acts of devotion.",
    ],
    "food and langar (community kitchen) culture at Kumbh Mela": [
        "Langars, or free community kitchens, feed millions of pilgrims every single day of Kumbh Mela at no cost.",
        "These kitchens are run entirely by volunteers and donations, reflecting the festival's spirit of selfless service.",
        "It's considered one of the largest volunteer-run food operations anywhere in the world during the festival period.",
    ],
    "how astrology (planetary positions) decides the Kumbh Mela dates": [
        "The exact dates of Kumbh Mela are determined by the positions of the Sun, Moon, and Jupiter in specific zodiac signs.",
        "This astrological calculation is why Kumbh Mela doesn't fall on a fixed calendar date and must be computed years in advance.",
        "Different planetary alignments determine which of the four cities hosts the Kumbh in a given cycle.",
    ],
    "a short devotional/inspirational message tied to Kumbh Mela values": [
        "Kumbh Mela is a reminder that people from every background - rich, poor, scholar, ascetic - can gather as equals in pursuit of something greater than themselves.",
        "At its heart, the festival teaches that purification isn't just physical - it's a chance to let go of what no longer serves you.",
        "Millions walk away from Kumbh Mela not with anything material, but with a renewed sense of purpose.",
    ],
    "safety and travel tips for pilgrims visiting Kumbh Mela": [
        "Given the enormous crowds, it's wise to fix a family meeting point in advance, since phone networks can get overloaded.",
        "Authorities set up massive lost-and-found centers, and announcement towers, specifically to reunite separated families.",
        "Traveling a day or two before or after the peak Shahi Snan dates can mean a similarly spiritual experience with far smaller crowds.",
    ],
    "a myth-busting fact about Kumbh Mela most people get wrong": [
        "Many assume Kumbh Mela happens every 12 years everywhere - but a smaller 'Ardh Kumbh' (half Kumbh) is actually held every 6 years at some sites.",
        "It's a common myth that only Hindu ascetics attend - in reality, Kumbh Mela draws visitors, researchers, and travelers of every faith and background.",
        "Contrary to popular belief, the festival isn't one single event - it unfolds over weeks, with multiple distinct bathing dates, each astrologically significant.",
    ],
}

HASHTAG_BANK = [
    "#KumbhMela", "#Kumbh2027", "#SanatanDharma", "#IncredibleIndia",
    "#HinduCulture", "#SpiritualIndia", "#Prayagraj", "#Haridwar",
    "#GangaSnan", "#NagaSadhu", "#UNESCOHeritage", "#FaithAndFestival",
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
