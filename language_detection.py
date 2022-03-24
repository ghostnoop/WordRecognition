import re

from en import en_profanity_checker, en_emotion_recognition
from text_mood import ru_profanity_checker, ru_emotion_recognition


def detect_language(text):
    en = "abcdefghijklmnopqrstuvwxyz"
    en_alphabet = list(en.strip())
    reg = re.compile(r'[^\w\s]')
    text = reg.sub('', text)

    en_counter = 0
    ru_counter = 0

    for symbol in text:
        if symbol in en_alphabet:
            en_counter += 1
        else:
            ru_counter += 1

    if en_counter >= ru_counter:
        profanity = en_profanity_checker(text)
        mood = en_emotion_recognition(text)
    else:
        profanity = ru_profanity_checker(text)
        mood = ru_emotion_recognition(text)

    return profanity, mood
