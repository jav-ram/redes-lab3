import threading
import time
from blessed import Terminal

t = Terminal()

def handle_table(self):
        print("handle_table flooding")

def OptionsMenu():
    while True:
        o = input("Option: ")
        if o == 'msg':
            send_individual_message()
        if o == 'table':
            handle_table()

    return
