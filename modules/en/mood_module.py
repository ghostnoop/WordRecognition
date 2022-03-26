import nltk
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


def en_emotion_recognition(text):
    emo = LeXmo.LeXmo(text)
    emo.pop('text', None)

    return emo

async def get_tone_of_en_text(text) -> str:
    sia = SentimentIntensityAnalyzer()
    result = sia.polarity_scores(text)
    result.pop('compound')
    return max(result.items(), key=operator.itemgetter(1))[0]


if __name__ == '__main__':
    print(en_profanity_checker('👍👍👍😍'))
    print(en_profanity_checker('Zidan juventus no👎'))
    print(en_profanity_checker('bad'))
    print(en_profanity_checker('good'))
    print(en_profanity_checker('Merry Christmas – wishing you good friends and happy memories'))


    print(get_tone_of_en_text('👍👍👍😍'))
    print(get_tone_of_en_text('Zidan juventus no👎'))
    print(get_tone_of_en_text('bad'))
    print(get_tone_of_en_text('good'))
    print(get_tone_of_en_text('Merry Christmas – wishing you good friends and happy memories'))
