import threading
import time
from blessed import Terminal

t = Terminal()

options = [
    ('h ', 'Volver a mostrar este menu'),               # Complete
    ('mi', 'Mensaje individual'),                       # Complete
    ('mg', 'Mensaje a grupo'),                          # Not Working
    ('ul', 'Lista de usuarios'),                        # Incomplete: parse
    ('ui', 'Información de usuario individual'),        # Incomplete: parse
    ('au', 'Agregar usuario a mi lista de contactos'),  # Complete
    ('st', 'Cambiar status'),                           # Maybe
    ('sf', 'Enviar archivo a una persona'),             # Not Working
    ('q ', 'Desconectarme'),                            # Incomplete: thread bum
    ('qq', 'Borrar cuenta'),                            # Complete
    # ('', ''),
]


def get_opt(target):
    for o in options:
        if target == o[0]:
            return target
    return None


def menu():
    print(t.bold('Menu de opciones:'))
    print('--------------------------------------')
    for o in options:
        print(t.bold(t.color(0)(o[0])) + '      ' + o[1])


def get_option(question=':'):
    return input(t.move(t.height - 1, 0) + question)


def switcher(opt, actions):
    if get_opt(opt) == None:
        print(t.color(9)('La opción no existe, pruebe con otra'))
        print('Si no sabe ingrese ' + t.bold(t.color(0)('h')) + ', para mas información')

    for o in options:
        if opt == o[0]:
            actions[opt]()


def OptionsMenu(h, mi, ul, sf, au, qq, st, ui, q):
    args = {
        'h ': h,
        'mi': mi,
        'ul': ul,
        'sf': sf,
        'au': au,
        'qq': qq,
        'st': st,
        'ui': ui,
        'q ': q,
    }
    menu()
    while True:
        option = get_option()
        switcher(option, args)
        if (option == 'q '):
            break
    #     print(self.args)
    #     switcher(option, self.args)

    return
