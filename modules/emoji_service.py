import sys
from collections import defaultdict

import emoji
import csv

import re

dic = {}
with open('files/emojies.csv', 'r', encoding='utf-8') as f:
    lines = f.read().strip().split('\n')
    for row in lines:
        a, b = row.split(';')
        dic[emoji.demojize(a).strip()] = b


def extract_emojis(text) -> dict:
    emojies = defaultdict(int)
    for symb in text:
        if symb in emoji.UNICODE_EMOJI['en']:
            emojies[symb] += 1

    return dict(emojies)


def emoji_checker(text, current_result):
    text = emoji.demojize(text)
    text = re.findall(r'(:[^:]*:)', text)
    list_emoji = [x for x in text]
    mood = {"positive": 0, "neutral": 0, "negative": 0}

    if list_emoji:
        for emj in list_emoji:
            emj = emj.strip()
            value = dic.get(emj, None)
            if value is not None:
                mood[value] += 1

        result = max(mood, key=mood.get)
    else:
        result = current_result

    return result

