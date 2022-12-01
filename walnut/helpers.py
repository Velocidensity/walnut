def pluralize(word: str, count: int) -> str:
    """Correctly pluralizes an English word based on a count of elements"""
    return word + 's' if count > 1 else word
