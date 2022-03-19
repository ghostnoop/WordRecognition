from emoji_service import extract_emojis
from text_mood import profanity_check, text_mood

if __name__ == "__main__":
    text = "Я купил новую машину. Она плохая"
    print(profanity_check(text),'profanity_check')
    print(text_mood(text))
    print(extract_emojis(text))
