
def is_lead_message(text: str | None, keywords: list[str], stop_words: list[str] | None = None) -> tuple[bool, str | None]:
    if not text:
        return False, None
    
    normalized  = " ".join(text.lower().split())

    if stop_words and any(word.lower() in normalized for word in stop_words):
        return False, None

    # return any(k_word in normalized for k_word in keywords)
    for k_word in keywords:
        if k_word.lower().strip() in normalized:
            return True, k_word
    return False, None
