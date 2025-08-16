\
import re
from unidecode import unidecode

def clean_tamil_text(s: str) -> str:
    if not isinstance(s, str):
        return ""
    # Replace tabs with space, collapse spaces, strip
    s = s.replace("\t", " ").replace("\u200b", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s

def normalize_for_search(s: str) -> str:
    if not isinstance(s, str):
        return ""
    s = clean_tamil_text(s)
    # Keep Tamil as-is; also keep a transliterated/ASCII fallback for English searches
    ascii_fallback = unidecode(s)
    return s + " " + ascii_fallback

def starts_with_words(haystack: str, prefix: str) -> bool:
    h = clean_tamil_text(haystack)
    p = clean_tamil_text(prefix)
    return h.startswith(p)
