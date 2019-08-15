import slixmpp
from threading import Thread
from slixmpp.exceptions import IqError, IqTimeout
from menu import OptionsMenu
from blessed import Terminal
from parse import get_dict, make_msg_json
import asyncio
import random

t = Terminal()


def msg_group(msg):
    print(t.color(40)(msg))


class User(slixmpp.ClientXMPP):

    def __init__(
        self,
        jid,
        password,
        algorithm,
        DEBUG=False,
        neighbors=[],
    ):
        super().__init__(jid, password)

        self.menu = Thread(target=OptionsMenu, args=(
            self.send_individual_message,
        ))

        self.algorithm = algorithm
        self.DEBUG = DEBUG
        self.neighbors = neighbors

        # start event
        self.add_event_handler('session_start', self.start)
        # register event
        self.add_event_handler('register', self.register)
        # message event
        self.add_event_handler('message', self.message)

    def start(self, event):
        self.send_presence()
        self.get_roster()
        print(self.boundjid)
        self.menu.start()  # Start while

    async def register(self, iq):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password

        try:
            await resp.send()
            print("Account created")
        except IqError:
            print("Error al crear cuenta, probablemente ya existe")
        except IqTimeout:
            print("timeout")
            self.disconnect()

    def message(self, msg):
        if msg['type'] in ('normal', 'chat'):
            # get type of message
            json = get_dict(msg[body])
            type = json['type']

            if type == 'message':
                # apply algorithm
                pass
            elif type == 'connection':
                # update neighbors
                pass
            elif type == 'response':
                # update neighbors
                pass

            print(t.color(random.randint(9, 15))(t.bold(str(msg['from'])) + ': ' + str(msg['body'])))
        else:
            # Error
            print('Error')
            print(msg['body'])

    def send_individual_message(self):
        mto = input('Para: ')
        mbody = input('Contenido: ')
        json_msg = make_msg_json(me=self.jid, to=mto, msg=mbody, hops=0, distance=0) # TODO: cambiar hops y distance
        self.send_message(mto=mto, mbody=json_msg)








