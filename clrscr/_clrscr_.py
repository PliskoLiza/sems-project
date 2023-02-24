import platform
import os


CLEAR_SCREEN_COMMAND = 'cls' if platform.system().lower() == 'windows' else 'clear'


def clrscr():
    os.system(CLEAR_SCREEN_COMMAND)
