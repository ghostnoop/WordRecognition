# from language_detection import detect_language
import re

import emoji

from worker import main_work

text='👍👍👍👍👍👍👍👍'
# a=detect_language(text)
d=main_work(text)
print(d)
