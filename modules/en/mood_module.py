import nltk

from modules.emoji_service import emoji_checker

nltk.download('vader_lexicon')

import operator

from better_profanity import profanity
from LeXmo import LeXmo
from nltk.sentiment import SentimentIntensityAnalyzer


def en_profanity_checker(text):
    censored = profanity.censor(text)
    flag = False

    if text != censored:
        flag = True

    return flag


TONE_DICT = {'negative': 'negative', 'neg': 'negative', 'positive': 'positive', 'pos': 'positive', 'neu': 'neutral',
             'skip': 'neutral', 'neutral': 'neutral'}


def en_emotion_recognition(text) -> str:
    sia = SentimentIntensityAnalyzer()
    result = sia.polarity_scores(text)
    result.pop('compound')
    result = TONE_DICT[max(result.items(), key=operator.itemgetter(1))[0]]
    if result == 'neutral':
        result = emoji_checker(text, result)

    return result


if __name__ == '__main__':
    print(en_profanity_checker('👍👍👍😍'))
    print(en_profanity_checker('Zidan juventus no👎'))
    print(en_profanity_checker('bad'))
    print(en_profanity_checker('good'))
    print(en_profanity_checker('Merry Christmas – wishing you good friends and happy memories'))
