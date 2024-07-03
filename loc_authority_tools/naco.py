import re

from unidecode import unidecode


# Characters that should be mapped differently from unidecode
non_unidecode_map = {
    # Translated Characters
    ord("\u0391"): "\u0391",  # alpha
    ord("\u03b1"): "\u0391",
    ord("\u0392"): "\u0392",  # beta
    ord("\u03b2"): "\u0392",
    ord("\u0393"): "\u0393",  # gamma
    ord("\u03b3"): "\u0393",

    # Punctuation
    ord("!"): " ",
    ord('"'): " ",
    ord("'"): "",
    ord("("): " ",
    ord(")"): " ",
    ord("-"): " ",
    ord("["): "",
    ord("]"): "",
    ord("{"): " ",
    ord("}"): " ",
    ord("<"): " ",
    ord(">"): " ",
    ord(";"): " ",
    ord(":"): " ",
    ord("."): " ",
    ord("?"): " ",
    ord("\u00bf"): " ",  # inverted question mark
    ord("\u00a1"): " ",  # inverted exclamation mark
    ord(","): " ",  # technically the first comma in the $a subfield is meant to be retained

    # Other Special Characters
    ord("\u266d"): "\u266d",  # musical flat
    ord("/"): " ",
    ord("\\"): " ",
    ord("$"): " ",
    ord("%"): " ",
    ord("*"): " ",
    ord("|"): " ",
    ord("%"): " ",
    ord("="): " ",
    ord("\u00b1"): " ",  # plus/minus sign
    ord("\u207a"): " ",  # super/subscript + - ( ) =
    ord("\u207b"): " ",
    ord("\u207c"): " ",
    ord("\u207d"): " ",
    ord("\u207e"): " ",
    ord("\u207f"): " ",
    ord("\u208a"): " ",
    ord("\u208b"): " ",
    ord("\u208c"): " ",
    ord("\u208d"): " ",
    ord("\u208e"): " ",
    ord("\u00ae"): " ",  # patent mark
    ord("\u2117"): " ",  # sound recording copyright
    ord("\u00a9"): " ",  # copyright sign
    ord("\u00a3"): "\u00a3",  # British pound sign
    ord("\u00b0"): " ",  # degree sign
    ord("_"): " ",
    ord("^"): " ",
    ord("`"): " ",
    ord("~"): " ",
    ord("\u005e"): " ",  # spacing circumflex
    ord("\uff3e"): " ",  # spacing circumflex
    ord("\u0060"): " ",  # spacing grave
    ord("\u007e"): " ",  # spacing tilde
    ord("\u00b4"): " ",  # spacing acute
    ord("\u02d8"): " ",  # spacing breve
    ord("\u20ac"): "\u20ac",  # Euro sign
    ord("\u266f"): "\u266f",  # musical sharp
    ord("\u0627"): "",  # alif
    ord("\ufe8e"): "",  # alif
    ord("\u02bf"): "",  # ayn
    ord("\u042a"): "",  # hard sign
    ord("\u044a"): "",  # hard sign
    ord("\u042c"): "",  # soft sign
    ord("\u044c"): "",  # soft sign
    ord("\u00b7"): " ",  # middle dot
}


def normalize(input_str):
    """
    Normalize a string using the NACO rules found at
    https://www.loc.gov/aba/pcc/naco/normrule-2.html.
    
    Note that:
        1) This function is MARC-code agnostic. Therefore, certain rules that are code-
        specific, such as retaining the first comma in $a fields, are not implemented.
        2) The NACO rules are incomplete and do not specify what to do with many of the
        ~150k unicode characters. This implementation heavily relies on unidecode to
        solve this problem. Whenever possible, we've used the given NACO rule to map a
        character, but otherwise we rely on unidecode to do so.
    """
    if input_str is None or len(input_str) == 0:
        return input_str

    if not isinstance(input_str, str):
        input_str = str(input_str, "utf-8")

    # We can't decode the whole string at once because certain non-ASCII characters need
    # to be retained, so go character by chacter instead.
    output_str = ""
    for char in input_str:
        if ord(char) not in non_unidecode_map:
            char = unidecode(char)
        if ord(char) in non_unidecode_map:
            char = non_unidecode_map[ord(char)]
        output_str += char

    return re.sub(" +", " ", output_str).strip().upper()
