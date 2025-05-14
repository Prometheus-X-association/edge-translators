from enum import Enum

class TerminalStyleEnum(str, Enum):
    NONE = "none"
    BOLD = "bold"
    UNDERLINE = "underline"

class TerminalColorEnum(str, Enum):
    RED = 'red'
    GREEN = 'green'
    YELLOW = 'yellow'
    BLUE = 'blue'
    MAGENTA = 'magenta'
    CYAN = 'cyan'
    RESET = 'reset'

COLOR_TO_ANSI = {
    TerminalColorEnum.RED: '\033[31m',
    TerminalColorEnum.GREEN: '\033[32m',
    TerminalColorEnum.YELLOW: '\033[33m',
    TerminalColorEnum.BLUE: '\033[34m',
    TerminalColorEnum.MAGENTA: '\033[35m',
    TerminalColorEnum.CYAN: '\033[36m',
}

STYLE_TO_ANSI = {
    TerminalStyleEnum.NONE: '',
    TerminalStyleEnum.BOLD: '\033[1m',
    TerminalStyleEnum.UNDERLINE: '\033[4m'
}

RESET_TO_ANSI = '\033[0m'


def niceprint(
    text: str,
    color: TerminalColorEnum = TerminalColorEnum.CYAN,
    style: TerminalStyleEnum = TerminalStyleEnum.NONE
):
    print(f"{STYLE_TO_ANSI[style]}{COLOR_TO_ANSI[color]}{text}{RESET_TO_ANSI}")
