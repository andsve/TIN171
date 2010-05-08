import os
import ctypes

def nt_set_color(color):
    COLORS = {
        "grey": 0x0007,
        "red": 0x000C,
        "green": 0x000A,
        "yellow": 0x000E,
        "blue": 0x0009,
        "magenta": 0x000D,
        "cyan": 0x0003,
        "white": 0x000F
    }
    
    STD_OUTPUT_HANDLE = -11
    stdout_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    SetConsoleTextAttribute = ctypes.windll.kernel32.SetConsoleTextAttribute
    SetConsoleTextAttribute(stdout_handle, COLORS[color])

def print_nt(text, color):
    nt_set_color(color)
    print(text)
    nt_set_color('grey')
    
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
            'white'
            ],
            range(30, 38)
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
        
