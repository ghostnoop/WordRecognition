from better_profanity import profanity
from LeXmo import LeXmo


def en_profanity_checker(text):
    censored = profanity.censor(text)
    flag = False

    if text != censored:
        flag = True

    return flag


def en_emotion_recognition(text):
    emo = LeXmo.LeXmo(text)
    emo.pop('text', None)

    result = max(emo, key=emo.get)

    return result