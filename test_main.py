from text_mood import profanity_check, text_mood

if __name__ == "__main__":
    text = "Я купил новую машину. Она мне очень нравится"
    print(profanity_check(text))
    print(text_mood(text))
