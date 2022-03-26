# -*- coding: cp1251 -*-

from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel

from modules.emoji_service import emoji_checker

with open('files/bad_words.csv', 'r', encoding='utf-8') as f:
    abusive_language = f.read().strip().split('\n')

import warnings
warnings.filterwarnings('ignore', '.*do not.*', 'Warning')

def distance(a, b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n, m)) space
        a, b = b, a
        n, m = m, n

    current_row = range(n + 1)  # Keep current and previous row, not entire matrix
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]


d = {'а': ['а', 'a', '@', '4'],
     'б': ['б', '6', 'b'],
     'в': ['в', 'b', 'v'],
     'г': ['г', 'r', 'g'],
     'д': ['д', 'd'],
     'е': ['е', 'e'],
     'ё': ['ё', 'e'],
     'ж': ['ж', 'zh', '*'],
     'з': ['з', '3', 'z'],
     'и': ['и', 'u', 'i'],
     'й': ['й', 'u', 'i'],
     'к': ['к', 'k', 'i{', '|{'],
     'л': ['л', 'l', 'ji'],
     'м': ['м', 'm'],
     'н': ['н', 'h', 'n'],
     'о': ['о', 'o', '0'],
     'п': ['п', 'n', 'p'],
     'р': ['р', 'r', 'p'],
     'с': ['с', 'c', 's'],
     'т': ['т', 'm', 't'],
     'у': ['у', 'y', 'u'],
     'ф': ['ф', 'f'],
     'х': ['х', 'x', 'h', '}{'],
     'ц': ['ц', 'c', 'u,'],
     'ч': ['ч', 'ch'],
     'ш': ['ш', 'sh'],
     'щ': ['щ', 'sch'],
     'ь': ['ь', 'b'],
     'ы': ['ы', 'bi'],
     'ъ': ['ъ'],
     'э': ['э', 'e'],
     'ю': ['ю', 'io'],
     'я': ['я', 'ya']
     }


def ru_profanity_checker(text):
    text = text.lower().replace(" ", "")

    for key, value in d.items():
        # Проходимся по каждой букве в значении словаря. То есть по вот этим спискам ['а', 'a', '@'].
        for letter in value:
            # Проходимся по каждой букве в нашей фразе.
            for phr in text:
                # Если буква совпадает с буквой в нашем списке.
                if letter == phr:
                    # Заменяем эту букву на ключ словаря.
                    text = text.replace(phr, key)

    flag = False

    for word in abusive_language:
        # Разбиваем слово на части, и проходимся по ним.
        for part in range(len(text)):
            # Вот сам наш фрагмент.
            fragment = text[part: part + len(word)]
            # Если отличие этого фрагмента меньше или равно 25% этого слова, то считаем, что они равны.
            if distance(fragment, word) <= len(word) * 0.25:
                # Если они равны, выводим надпись о их нахождении.
                flag = True

        if flag:
            break

    return flag


def ru_emotion_recognition(text):

    FastTextSocialNetworkModel.MODEL_PATH = 'files/fasttext-social-network-model.bin'
    tokenizer = RegexTokenizer()
    model = FastTextSocialNetworkModel(tokenizer=tokenizer)

    messages = [
        text
    ]

    results = model.predict(messages, k=2)

    for message, sentiment in zip(messages, results):
        if 'skip' in sentiment:
            del sentiment['skip']

    result = max(sentiment, key=sentiment.get)

    if result == 'neutral':
        result = emoji_checker(text, result)

    return result
