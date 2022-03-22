import re


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
        result = 'en'
    else:
        result = 'ru'

    return result
