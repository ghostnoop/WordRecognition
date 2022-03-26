from language_detection import detect_language
from modules.emoji_service import extract_emojis

emotion_dct = {
    "negative": 1,
    "positive": 2,
    "neutral": 3
}


def main_work(text):
    profanity, mood = detect_language(text)
    emojis = extract_emojis(text)
    return profanity, mood, emojis
