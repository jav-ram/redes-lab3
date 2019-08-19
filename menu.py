import threading
import time
from blessed import Terminal

t = Terminal()


def OptionsMenu(s_msg, s_table):
    while True:
        o = input("Option: ")
        if o == 'msg':
            s_msg()
        if o == 'table':
            s_table()

    return
