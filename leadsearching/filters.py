
def is_lead_message(text: str | None, keywords: list[str], stop_words: list[str] | None = None) -> bool:
    if not text:
        return False
    
    normalized  = text.lower()

    if stop_words and any(word.lower() in normalized for word in stop_words):
        return False

    return any(k_word in normalized for k_word in keywords)
