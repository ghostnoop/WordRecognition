import re

from modules.en.mood_module import en_profanity_checker, en_emotion_recognition
from modules.ru.mood_module import ru_profanity_checker, ru_emotion_recognition


def detect_language(text):
    print('detect',text)
    en = "abcdefghijklmnopqrstuvwxyz"
    en_alphabet = list(en.strip())
    ru = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    ru_alphabet = list(en.strip())
    reg = re.compile(r'[^\w\s]')
    text = reg.sub('', text)

    en_counter = 0
    ru_counter = 0

    for symbol in text:
        if symbol in en_alphabet:
            en_counter += 1
        else:
            ru_counter += 1

    if en_counter > ru_counter:
        print('en')
        profanity = en_profanity_checker(text)
        mood = en_emotion_recognition(text)
    else:
        print('ru')
        profanity = ru_profanity_checker(text)
        mood = ru_emotion_recognition(text)

    return profanity, mood
