import re


def normalize_whitespace(text):
    """ Normalize the whitespace in a string."""
    return re.sub(r'\s+', ' ', text.strip())