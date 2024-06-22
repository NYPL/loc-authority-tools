import re
import unicodedata

import nameparser

def tokenize_name(name: str) -> list[str]:
    hn = nameparser.HumanName(name)
    tokens = []
    for part in (hn.first, hn.middle, hn.last, hn.nickname):
        if not part or not all(char.isalpha() for char in part):
            continue
        for word in split(part):
            cleaned = clean_word(word)
            if cleaned:
                tokens.append(cleaned)

    return tokens


def split(s: str) -> list[str]:
    return list(re.split(r"(\s|\,)", s.strip()))


def clean_word(word: str) -> str:
    delete_characters = "'[]"
    space_characters = r"!\"()-{}<>;:.\?¿¡/\\*|%=+~"
    word = word.strip().lower()
    word = re.sub(f"[{delete_characters}]", "", word)
    word = re.sub(f"[{re.escape(space_characters)}]", " ", word)
    word = re.sub(r"\s+", " ", word)
    return convert_unicode(word).strip()


def convert_unicode(word: str) -> str:
    return unicodedata.normalize('NFKD', word).encode("ascii", "ignore").decode()
