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


d = {'�': ['�', 'a', '@', '4'],
     '�': ['�', '6', 'b'],
     '�': ['�', 'b', 'v'],
     '�': ['�', 'r', 'g'],
     '�': ['�', 'd'],
     '�': ['�', 'e'],
     '�': ['�', 'e'],
     '�': ['�', 'zh', '*'],
     '�': ['�', '3', 'z'],
     '�': ['�', 'u', 'i'],
     '�': ['�', 'u', 'i'],
     '�': ['�', 'k', 'i{', '|{'],
     '�': ['�', 'l', 'ji'],
     '�': ['�', 'm'],
     '�': ['�', 'h', 'n'],
     '�': ['�', 'o', '0'],
     '�': ['�', 'n', 'p'],
     '�': ['�', 'r', 'p'],
     '�': ['�', 'c', 's'],
     '�': ['�', 'm', 't'],
     '�': ['�', 'y', 'u'],
     '�': ['�', 'f'],
     '�': ['�', 'x', 'h', '}{'],
     '�': ['�', 'c', 'u,'],
     '�': ['�', 'ch'],
     '�': ['�', 'sh'],
     '�': ['�', 'sch'],
     '�': ['�', 'b'],
     '�': ['�', 'bi'],
     '�': ['�'],
     '�': ['�', 'e'],
     '�': ['�', 'io'],
     '�': ['�', 'ya']
     }


def ru_profanity_checker(text):
    text = text.lower().replace(" ", "")

    for key, value in d.items():
        # ���������� �� ������ ����� � �������� �������. �� ���� �� ��� ���� ������� ['�', 'a', '@'].
        for letter in value:
            # ���������� �� ������ ����� � ����� �����.
            for phr in text:
                # ���� ����� ��������� � ������ � ����� ������.
                if letter == phr:
                    # �������� ��� ����� �� ���� �������.
                    text = text.replace(phr, key)

    flag = False

    for word in abusive_language:
        # ��������� ����� �� �����, � ���������� �� ���.
        for part in range(len(text)):
            # ��� ��� ��� ��������.
            fragment = text[part: part + len(word)]
            # ���� ������� ����� ��������� ������ ��� ����� 25% ����� �����, �� �������, ��� ��� �����.
            if distance(fragment, word) <= len(word) * 0.25:
                # ���� ��� �����, ������� ������� � �� ����������.
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
