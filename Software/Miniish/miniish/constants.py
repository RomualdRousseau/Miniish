from pyco.constants import BLACK, BLUE, DARK_GRAY, DARK_PURPLE, GREEN, INDIGO, LIGHT_GRAY, PINK, RED, WHITE

OS_NAME = "miniish"
OS_VERSION = "0.1"

BANNER = f"""
@logo                       
                            
{OS_NAME} {OS_VERSION}
(c) 2022-24 romuald rousseau
"""

PROMPT = "\r> "

DEFAULT_LANGUAGE = "asm6502"

DEFAULT_PORT = "/dev/ttyUSB0"
DEFAULT_BAUD_RATE = 19200

MAX_BUFFERS = 8

COLOR_CONS_BG = BLACK
COLOR_CONS_FG = WHITE
COLOR_MAIN_BG = DARK_GRAY
COLOR_MAIN_FG = LIGHT_GRAY
COLOR_STAT_BG = RED
COLOR_STAT_FG = DARK_PURPLE
COLOR_CURSOR = RED

SYNTAX_TOKEN = LIGHT_GRAY
SYNTAX_SYMBOL = WHITE
SYNTAX_NUMBER = BLUE
SYNTAX_STRING = BLUE
SYNTAX_KEYWORD1 = GREEN
SYNTAX_KEYWORD2 = PINK
SYNTAX_COMMENT = INDIGO
