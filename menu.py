import threading
import time


def handle_table(self):
    print("handle_table flooding")


def OptionsMenu(send_individual_message, handle_table):
    while True:
        print("\nOpciones:")
        print("msg - Mandar Mensaje")
        print("table - Ver Tabla\n")
        o = input("Option: ")
        if o == 'msg':
            send_individual_message()
        if o == 'table':
            handle_table()

    return
