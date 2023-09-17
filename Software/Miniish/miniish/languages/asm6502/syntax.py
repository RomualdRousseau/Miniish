import pyco

from miniish.constants import (
    SYNTAX_COMMENT,
    SYNTAX_KEYWORD1,
    SYNTAX_KEYWORD2,
    SYNTAX_NUMBER,
    SYNTAX_STRING,
    SYNTAX_SYMBOL,
    SYNTAX_TOKEN,
)


KEYWORDS1 = (
    "ADC",
    "AND",
    "ASL",
    "BBR",
    "BBS",
    "BCC",
    "BCS",
    "BEQ",
    "BIT",
    "BMI",
    "BNE",
    "BPL",
    "BRA",
    "BRK",
    "BVC",
    "BVS",
    "CLC",
    "CLD",
    "CLI",
    "CLV",
    "CMP",
    "CPX",
    "CPY",
    "DEC",
    "DEX",
    "DEY",
    "EOR",
    "INC",
    "INX",
    "INY",
    "JMP",
    "JSR",
    "LDA",
    "LDX",
    "LDY",
    "LSR",
    "NOP",
    "ORA",
    "PHA",
    "PHX",
    "PHY",
    "PHP",
    "PLA",
    "PLX",
    "PLY",
    "PLP",
    "ROL",
    "ROR",
    "RMB",
    "RTI",
    "RTS",
    "SBC",
    "SEC",
    "SED",
    "SEI",
    "SMB",
    "STA",
    "STP",
    "STX",
    "STY",
    "STZ",
    "TAX",
    "TAY",
    "TRB",
    "TSB",
    "TSX",
    "TXA",
    "TXS",
    "TYA",
    "WAI",
)

KEYWORDS2 = ("ORG", "ASCIIZ", "BYTE", "WORD", "DSECT", "DEND", "INCLUDE")


def colorize(line: str, pos: tuple[int, int]) -> None:
    token = ""
    state = 0

    def colorize_keyword(token):
        return (
            SYNTAX_KEYWORD1
            if _is_keyword1(token)
            else SYNTAX_KEYWORD2
            if _is_keyword2(token)
            else SYNTAX_TOKEN
        )

    def emit_token(token, pos, next_token=""):
        if state == 0:
            pyco.print(token, pos, colorize_keyword(token))
        elif state == 1:
            pyco.print(token, pos, SYNTAX_COMMENT)
        elif state == 2:
            pyco.print(token, pos, SYNTAX_NUMBER)
        elif state == 3:
            pyco.print(token, pos, SYNTAX_STRING)
        return next_token, (pos[0] + len(token) * 4, pos[1])

    for c in line:
        if state == 0:
            if c.isspace():  # Spaces flush the current token
                token, pos = emit_token(token, pos)
                pos = (pos[0] + 4, pos[1])
            elif _is_comment(c):
                token, pos = emit_token(token, pos, c)
                state = 1
            elif _is_string(c):
                token, pos = emit_token(token, pos, c)
                state = 3
            elif _is_number(c) and len(token) == 0:
                token, pos = emit_token(token, pos, c)
                state = 2
            elif _is_symbol(c):
                token, pos = emit_token(token, pos)
                pyco.print(c, pos, SYNTAX_SYMBOL)
                pos = (pos[0] + 4, pos[1])
            else:
                token += c

        elif state == 1:  # Comment
            token += c

        elif state == 2:  # Number
            if c.isspace():  # Spaces flush the current token
                token, pos = emit_token(token, pos)
                pos = (pos[0] + 4, pos[1])
                state = 0
            elif _is_comment(c):
                token, pos = emit_token(token, pos, c)
                state = 1
            elif _is_string(c):
                token, pos = emit_token(token, pos, c)
                state = 3
            elif _is_symbol(c):
                token, pos = emit_token(token, pos)
                pyco.print(c, pos, SYNTAX_SYMBOL)
                pos = (pos[0] + 4, pos[1])
                state = 0
            else:
                token += c

        elif state == 3:  # String
            if _is_string(c):
                token, pos = emit_token(token + c, pos)
                state = 0
            else:
                token += c

    emit_token(token, pos)


def _is_comment(token: str) -> bool:
    return token == ";"


def _is_string(token: str) -> bool:
    return token in ('"', "'")


def _is_number(token: str) -> bool:
    return token.isnumeric() or token in ("%", "$")


def _is_symbol(token: str) -> bool:
    return not (token.isalpha() or token.isnumeric() or token == "_")


def _is_keyword1(token: str) -> bool:
    return token.upper() in KEYWORDS1


def _is_keyword2(token: str) -> bool:
    return token.upper() in KEYWORDS2
