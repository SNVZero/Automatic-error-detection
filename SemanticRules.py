import re

def find_duplicate_words(text):
    pattern = r'\b(\w+)\s+\1\b'
    return re.findall(pattern, text, flags=re.IGNORECASE)

def find_space_before_punctuation(text):
    pattern = r'\s+[.,!?;:]'
    return re.findall(pattern, text)


def find_missing_space_after_punctuation(text):
    pattern = r'[.,!?;:](?!\s|$)'
    return re.findall(pattern, text)


def find_unexpected_capitals(text):
    pattern = r'(?<![.!?])\s+[A-Z][a-z]+'
    return re.findall(pattern, text)


def find_unbalanced_quotes(text):
    return text.count('"') % 2 != 0 or text.count('«') != text.count('»')