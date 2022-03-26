from collections import defaultdict

import emoji
import csv

import re


def extract_emojis(text) -> dict:
    emojies = defaultdict(int)
    for symb in text:
        if symb in emoji.UNICODE_EMOJI['en']:
            emojies[symb] += 1

    return dict(emojies)


def emoji_checker(text, current_result):
    dic = {}
    with open('files/emojies.csv', 'r', newline='') as csvfile:
        fieldnames = ['emoji', 'value']
        reader = csv.DictReader(csvfile, fieldnames)
        for row in reader:
            dic[row["emoji"]] = row['value']

    text = emoji.demojize(text)
    text = re.findall(r'(:[^:]*:)', text)
    list_emoji = [emoji.emojize(x) for x in text]
    mood = {"positive": 0, "neutral": 0, "negative": 0}

    if list_emoji:
        for emj in list_emoji:
            value = dic.get(emj)
            if emj is not None:
                mood[value] += 1

        result = max(mood, key=mood.get)
    else:
        result = current_result

    return result