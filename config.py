"""
Central config for the Kumbh Mela content pipeline.
Edit TOPIC_SEEDS any time to steer what the AI talks about.
Content is written in Hindi (Devanagari) for the voiceover/script.
"""

# Seed themes (kept in English internally as stable keys; the actual
# script/voiceover text is Hindi - see TOPIC_FACTS_HI below).
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

# Hindi on-screen titles per seed.
TOPIC_TITLES_HI = {
    "the history and origin of Kumbh Mela": "कुंभ मेले की उत्पत्ति",
    "the mythology of Samudra Manthan and how it connects to Kumbh Mela": "समुद्र मंथन की कथा",
    "the four Kumbh Mela locations: Prayagraj, Haridwar, Ujjain, Nashik": "कुंभ के चार पवित्र स्थान",
    "Naga Sadhus - who they are and their way of life": "नागा साधु कौन हैं?",
    "the Akharas (monastic orders) of Kumbh Mela": "कुंभ के अखाड़े",
    "Shahi Snan (the royal bath) - what it is and why it matters": "शाही स्नान का महत्व",
    "how Kumbh Mela became a UNESCO Intangible Cultural Heritage": "यूनेस्को धरोहर बना कुंभ",
    "the scale of Kumbh Mela - crowd numbers, logistics, temporary city facts": "कुंभ मेले का विशाल स्तर",
    "spiritual significance of bathing in the Ganga during Kumbh": "गंगा स्नान का आध्यात्मिक महत्व",
    "lesser-known rituals and traditions at Kumbh Mela": "कुंभ की अनसुनी परंपराएं",
    "food and langar (community kitchen) culture at Kumbh Mela": "कुंभ का लंगर",
    "how astrology (planetary positions) decides the Kumbh Mela dates": "ज्योतिष कैसे तय करता है तारीख",
    "a short devotional/inspirational message tied to Kumbh Mela values": "कुंभ का संदेश",
    "safety and travel tips for pilgrims visiting Kumbh Mela": "सुरक्षा और यात्रा टिप्स",
    "a myth-busting fact about Kumbh Mela most people get wrong": "कुंभ मेले का एक मिथक",
}

# Backup fact bank (Hindi) used to LOCALLY write a script if the free AI
# text API is unavailable or changes its terms again (keeps the pipeline
# 100% free and never dependent on a single third party staying free).
TOPIC_FACTS = {
    "the history and origin of Kumbh Mela": [
        "कुंभ मेले की जड़ें हजार साल से भी पुरानी हैं, जो देवताओं और असुरों के बीच अमृत कलश के लिए हुए संघर्ष की कथा से जुड़ी हैं।",
        "माना जाता है कि उस अमृत की कुछ बूंदें धरती पर चार जगहों पर गिरीं - प्रयागराज, हरिद्वार, उज्जैन और नासिक - इसीलिए यह मेला इन्हीं चार स्थानों के बीच घूमता है।",
        "आठवीं सदी के महान दार्शनिक आदि शंकराचार्य को अक्सर संतों के इन जमावड़ों को एक संगठित पर्व का रूप देने का श्रेय दिया जाता है।",
    ],
    "the mythology of Samudra Manthan and how it connects to Kumbh Mela": [
        "समुद्र मंथन की कथा देवताओं और असुरों द्वारा मिलकर अमृत पाने के लिए समुद्र मंथन करने की कहानी है।",
        "जब अमृत कलश ले जाया जा रहा था, तो कुछ बूंदें धरती की चार जगहों पर गिरीं - वही स्थान जहां आज कुंभ मेला आयोजित होता है।",
        "इसीलिए भक्तों का मानना है कि इन स्थानों पर स्नान करना उसी अमृत जैसा पवित्र प्रभाव रखता है।",
    ],
    "the four Kumbh Mela locations: Prayagraj, Haridwar, Ujjain, Nashik": [
        "कुंभ मेला चार पवित्र नदियों के तट पर बारी-बारी से आयोजित होता है - प्रयागराज और हरिद्वार में गंगा, उज्जैन में शिप्रा, और नासिक में गोदावरी।",
        "हर स्थान पर पूर्ण कुंभ लगभग हर बारह साल में एक बार आता है, यानी एक जीवनकाल में कोई इसे मुश्किल से कुछ ही बार देख पाता है।",
        "प्रयागराज का कुंभ सबसे बड़ा माना जाता है, जो संगम पर होता है - गंगा, यमुना और पौराणिक सरस्वती नदी के मिलन स्थल पर।",
    ],
    "Naga Sadhus - who they are and their way of life": [
        "नागा साधु ऐसे योद्धा-तपस्वी होते हैं जो सांसारिक मोह त्यागकर वस्त्र तक का त्याग कर देते हैं, यह पूर्ण वैराग्य का प्रतीक है।",
        "नागा साधु बनने में अक्सर एक दशक से भी ज्यादा समय लगता है - गुरु के मार्गदर्शन में कठोर साधना और अनुशासन से गुजरना पड़ता है।",
        "हर कुंभ मेले में शाही स्नान का नेतृत्व यही नागा साधु करते हैं।",
    ],
    "the Akharas (monastic orders) of Kumbh Mela": [
        "अखाड़े सदियों पुराने साधु-संतों के संगठित समूह हैं, हर एक की अपनी परंपरा, आराध्य देवता और पदानुक्रम होता है।",
        "आज तेरह प्रमुख अखाड़े मान्यता प्राप्त हैं, जिनमें से कुछ की स्थापना आठवीं सदी तक जाती है।",
        "कुंभ मेले में अखाड़े विशाल शिविर लगाते हैं और एक तय क्रम में भव्य शोभायात्रा निकालते हैं।",
    ],
    "Shahi Snan (the royal bath) - what it is and why it matters": [
        "शाही स्नान कुंभ मेले का सबसे पवित्र स्नान अनुष्ठान है, जिसका समय ज्योतिषीय गणना से तय किया जाता है।",
        "सबसे पहले नागा साधु और अखाड़ों के प्रमुख स्नान करते हैं, उसके बाद करोड़ों श्रद्धालु उसी पुण्य की आशा में स्नान करते हैं।",
        "इसकी शुभ तिथियां ग्रहों की स्थिति के आधार पर महीनों या सालों पहले तय कर ली जाती हैं।",
    ],
    "how Kumbh Mela became a UNESCO Intangible Cultural Heritage": [
        "2017 में यूनेस्को ने कुंभ मेले को मानवता की अमूर्त सांस्कृतिक धरोहर की सूची में शामिल किया।",
        "इसे इसके विशाल स्तर, विविध अनुष्ठानों और श्रद्धालुओं के बीच सार्वभौमिक भाईचारे को बढ़ावा देने के लिए मान्यता दी गई।",
        "यूनेस्को ने खासतौर पर इस बात को सराहा कि यहां इतनी अलग-अलग साधु परंपराएं शांति से एक साथ मौजूद रहती हैं।",
    ],
    "the scale of Kumbh Mela - crowd numbers, logistics, temporary city facts": [
        "कुंभ मेला पृथ्वी पर मनुष्यों का सबसे बड़ा शांतिपूर्ण जमावड़ा माना जाता है, जिसमें पिछले आयोजनों में दस करोड़ से भी ज्यादा लोग शामिल हुए।",
        "इस आयोजन के लिए शुरू से एक अस्थायी शहर बसाया जाता है - सड़कें, पुल, अस्पताल और अपनी खुद की पुलिस व्यवस्था के साथ।",
        "सबसे बड़े स्नान वाले दिन, कुछ ही घंटों में करोड़ों लोग नदी किनारे इकट्ठा हो सकते हैं।",
    ],
    "spiritual significance of bathing in the Ganga during Kumbh": [
        "माना जाता है कि कुंभ मेले के दौरान गंगा में स्नान करने से जन्मों-जन्मों के पाप धुल जाते हैं।",
        "श्रद्धालु सिर्फ उसी शुभ क्षण में स्नान करने के लिए देश-विदेश से यात्रा करके आते हैं।",
        "कई लोगों के लिए यह सिर्फ एक रस्म नहीं, बल्कि मोक्ष पाने का एक अनमोल अवसर है।",
    ],
    "lesser-known rituals and traditions at Kumbh Mela": [
        "प्रसिद्ध शाही स्नान के अलावा, कुंभ मेले में कई दिनों तक धार्मिक प्रवचन, भजन-कीर्तन और विद्वानों के बीच शास्त्रार्थ भी होता है।",
        "कई श्रद्धालु अपने पूर्वजों को श्रद्धांजलि देने के लिए पिंड दान की रस्म भी निभाते हैं।",
        "कुछ साधु कुंभ के दौरान वर्षों तक चलने वाले कठिन व्रत लेते हैं - जैसे कभी न बैठना, या हमेशा एक हाथ ऊपर उठाए रखना - भक्ति के प्रतीक के रूप में।",
    ],
    "food and langar (community kitchen) culture at Kumbh Mela": [
        "लंगर यानी मुफ्त सामुदायिक रसोई कुंभ मेले में रोज़ाना लाखों श्रद्धालुओं को भोजन कराती है, बिना किसी शुल्क के।",
        "ये रसोई पूरी तरह स्वयंसेवकों और दान से चलती हैं, जो इस पर्व की निःस्वार्थ सेवा भावना को दर्शाती हैं।",
        "यह दुनिया के सबसे बड़े स्वयंसेवी भोजन अभियानों में से एक माना जाता है।",
    ],
    "how astrology (planetary positions) decides the Kumbh Mela dates": [
        "कुंभ मेले की सटीक तारीखें सूर्य, चंद्रमा और बृहस्पति की राशियों में विशेष स्थिति के आधार पर तय होती हैं।",
        "इसी वजह से कुंभ मेला किसी तय कैलेंडर तारीख पर नहीं आता, बल्कि इसकी गणना सालों पहले करनी पड़ती है।",
        "अलग-अलग ग्रहों की स्थिति यह भी तय करती है कि किसी चक्र में कुंभ किस शहर में लगेगा।",
    ],
    "a short devotional/inspirational message tied to Kumbh Mela values": [
        "कुंभ मेला यह याद दिलाता है कि हर पृष्ठभूमि के लोग - अमीर, गरीब, विद्वान, तपस्वी - सब एक साथ, बराबरी से, कुछ बड़े उद्देश्य के लिए इकट्ठा हो सकते हैं।",
        "इसका मूल संदेश यही है कि शुद्धि सिर्फ शरीर की नहीं, बल्कि उन चीज़ों को छोड़ने का अवसर भी है जो अब हमारे काम की नहीं रहीं।",
        "करोड़ों लोग कुंभ मेले से कुछ भौतिक लेकर नहीं, बल्कि जीवन का एक नया उद्देश्य लेकर लौटते हैं।",
    ],
    "safety and travel tips for pilgrims visiting Kumbh Mela": [
        "इतनी बड़ी भीड़ को देखते हुए, पहले से परिवार के मिलने की एक जगह तय कर लेना समझदारी है, क्योंकि फोन नेटवर्क अक्सर व्यस्त हो जाता है।",
        "प्रशासन खोया-पाया केंद्र और अनाउंसमेंट टावर खासतौर पर बिछड़े परिवारों को मिलाने के लिए लगाता है।",
        "मुख्य शाही स्नान की तारीखों से एक-दो दिन आगे-पीछे यात्रा करने पर भी वैसा ही आध्यात्मिक अनुभव मिल सकता है, वो भी कम भीड़ के साथ।",
    ],
    "a myth-busting fact about Kumbh Mela most people get wrong": [
        "बहुत से लोग सोचते हैं कि कुंभ मेला हर जगह बारह साल में आता है - लेकिन कुछ स्थानों पर हर छह साल में एक छोटा 'अर्ध कुंभ' भी आयोजित होता है।",
        "यह भी एक आम भ्रम है कि यहां सिर्फ हिंदू तपस्वी आते हैं - असल में कुंभ मेला हर धर्म और हर जगह से आए यात्रियों और शोधकर्ताओं को आकर्षित करता है।",
        "आम धारणा के विपरीत, यह कोई एक दिन का आयोजन नहीं है - यह हफ्तों तक चलता है, जिसमें कई अलग स्नान तिथियां होती हैं, हर एक का अपना ज्योतिषीय महत्व है।",
    ],
}

HOOKS_HI = [
    "कुंभ मेले के बारे में एक ऐसी बात जो शायद आप नहीं जानते।",
    "यह कुंभ मेले के सबसे दिलचस्प तथ्यों में से एक है।",
    "शायद आपने कुंभ मेले के बारे में यह पहले कभी नहीं सुना होगा।",
    "आइए बात करते हैं कुंभ मेले की एक अद्भुत बात की।",
]

CLOSERS_HI = [
    "यही है कुंभ मेले की कहानी - आस्था, इतिहास और ऐसा भव्य स्तर जो दुनिया में कहीं और नहीं मिलता।",
    "यही वजह है कि कुंभ मेला इंसानी इतिहास के सबसे असाधारण जमावड़ों में गिना जाता है।",
    "हमारे साथ जुड़े रहिए, कुंभ मेले की और भी अनसुनी बातें जानने के लिए।",
]

HASHTAG_BANK = [
    "#कुंभमेला", "#प्रयागराज", "#हरिद्वार", "#सनातनधर्म", "#भारतीयसंस्कृति",
    "#आध्यात्मिकता", "#गंगा", "#नागासाधु", "#KumbhMela", "#IncredibleIndia",
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
