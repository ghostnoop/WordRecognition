from emoji_service import extract_emojis
from language_detection import detect_language

if __name__ == "__main__":
    text = """From the beginning, she had sat looking at him fixedly.
      As he now leaned back in his chair, and bent his deep-set eyes upon her in his turn,
      perhaps he might have seen one wavering moment in her,
      when she was impelled to throw herself upon his breast,
      and give him the pent-up confidences of her heart.
      But, to see it, he must have overleaped at a bound the artificial barriers he had for many years been erecting,
      between himself and all those subtle essences of humanity which will elude the utmost cunning of algebra
      until the last trumpet ever to be sounded shall blow even algebra to wreck.
      The barriers were too many and too high for such a leap. With his unbending,
      utilitarian, matter-of-fact face, he hardened her again;
      and the moment shot away into the plumbless depths of the past,
      to mingle with all the lost opportunities that are drowned there fuck."""
    profanity, mood = detect_language(text)
    print(profanity, mood)
