from emoji_service import extract_emojis
from text_mood import profanity_check, text_mood

if __name__ == "__main__":
    text = "Я купил новую машину. Она плохая 😀 мандей"
    print(profanity_check(text))
    print(text_mood(text))
    print(extract_emojis(text))
