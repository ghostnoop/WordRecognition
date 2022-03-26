import re

from modules.en.mood_module import en_profanity_checker, en_emotion_recognition
from modules.ru.mood_module import ru_profanity_checker, ru_emotion_recognition


def detect_language(text):
    print('detect', text)
    en = "abcdefghijklmnopqrstuvwxyz"
    en_alphabet = list(en.strip())
    ru = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    ru_alphabet = list(en.strip())
    reg = re.compile(r'[^\w\s]')
    text_copy = reg.sub('', text)

    en_counter = 0
    ru_counter = 0

    for symbol in text_copy:
        if symbol in en_alphabet:
            en_counter += 1
        else:
            ru_counter += 1

    if en_counter > ru_counter:
        print('en', text)
        profanity = en_profanity_checker(text)
        print('en profanity', text)
        mood = en_emotion_recognition(text)
        print('en mood', text)

    else:
        print('ru', text)
        profanity = ru_profanity_checker(text)
        print('ru profanity', text)
        mood = ru_emotion_recognition(text)
        print('ru mood ', text)

    return profanity, mood
