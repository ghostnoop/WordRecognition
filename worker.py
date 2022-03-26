from language_detection import detect_language
from modules.emoji_service import extract_emojis

emotion_dct = {
    "negative": 1,
    "positive": 2,
    "neutral": 3
}


def main_work(text):
    print('in main', text)
    profanity, mood = detect_language(text)
    emojis = extract_emojis(text)
    try:
        mood = emotion_dct[mood.lower()]
    except:
        mood = 3
    return profanity, mood, emojis
