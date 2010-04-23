import os
import ctypes

def print_nt(text, color):
    COLORS = {
        "grey": 0x0007,
        "red": 0x0004,
        "green": 0x0002,
        "yellow": 0x0006,
        "blue": 0x0001,
        "magenta": 0x0005,
        "cyan": 0x0003
    }
    
    STD_OUTPUT_HANDLE = -11
    stdout_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    SetConsoleTextAttribute = ctypes.windll.kernel32.SetConsoleTextAttribute
    SetConsoleTextAttribute(stdout_handle, COLORS[color])
    print(text)
    SetConsoleTextAttribute(stdout_handle, COLORS['grey'])
    
def print_posix(text, color):
    RESET = '\033[0m'
    COLORS = dict(
        zip([
            'grey',
            'red',
            'green',
            'yellow',
            'blue',
            'magenta',
            'cyan',
            ],
            range(30, 37)
            )
        )
        
    if os.getenv('ANSI_COLORS_DISABLED') is None:
        fmt_str = '\033[%dm%s'
        if color is not None:
            text = fmt_str % (COLORS[color], text)
        text += RESET
        
    print(text)

def cprint(text, color):
    if os.name == 'nt':
        print_nt(text, color)
    else:
        print_posix(text, color)
        