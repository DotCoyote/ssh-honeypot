from honeypot import PREVIEW_MAX_LENGTH

def cleanup_text(text: str, max_length: int = PREVIEW_MAX_LENGTH):
    'Clean up the text for display, truncating it if it exceeds max_length and appending an ellipsis and the number of truncated characters.'
    if len(text) > max_length:
        return repr(text[:max_length]) + "... (+" + str(len(text) - max_length) + " chars)"
    return repr(text)
