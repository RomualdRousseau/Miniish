from miniish.constants import DEFAULT_LANGUAGE
from miniish.languages.language import Language
from miniish.languages.python import Python
from miniish.languages.asm6502 import Asm6502


LANGUAGES: dict[str, Language] = {"python": Python(), "asm6502": Asm6502()}


class LANGUAGE:
    language: Language = LANGUAGES[DEFAULT_LANGUAGE]


def get_current_language() -> Language:
    return LANGUAGE.language


def change_language(lang: str) -> bool:
    LANGUAGE.language = LANGUAGES.get(lang) or LANGUAGES[DEFAULT_LANGUAGE]
    return lang == LANGUAGE.language.get_name()
