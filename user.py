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

        self.register_plugin('xep_0030')  # Service Discovery
        self.register_plugin('xep_0004')  # Data forms
        self.register_plugin('xep_0060')  # PubSub
        self.register_plugin('xep_0065')  # File transfer
        self.register_plugin('xep_0199')  # XMPP Ping
        self.register_plugin('xep_0047')  # In-band Bytestreams
        self.register_plugin('xep_0066')  # Out-of-band Data
        self.register_plugin('xep_0077')  # Register
        self.register_plugin('xep_0065')  # SOCKS5 Bytestreams
        self.plugin['xep_0077'].force_registration = True

        self.menu = Thread(target=OptionsMenu, args=(
            self.send_individual_message,
        ))

        self.algorithm = algorithm
        self.DEBUG = DEBUG
        self.neighbors = neighbors
        self.me = jid

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
            # parceo string to json
            message = get_dict(msg["body"])
            message_type = message['type']
            if message_type == 'message':
                # para flooding
                if message['to'] != self.jid:
                    for neighbor in self.neighbors:
                        # enviar a todos los vecinos que no sean el origen, que no sea el vecino que mando el ultimo menasje y que no sea el vecino que creo el mensaje
                        if (
                            self.me != neighbor and
                            message['from'] != neighbor and
                            message['origin'] != neighbor
                        ):
                            json_msg = make_msg_json(
                                origin=message['origin'],
                                me=self.me, to="all",
                                msg=message["msg"],
                                hops=message['hops']+1
                            )
                            self.send_message(mto=neighbor, mbody=json_msg)
                else:
                    print(message)
                        
                # apply algorithm
                pass
            elif message_type == 'connection':
                # update neighbors
                pass
            elif message_type == 'response':
                # update neighbors
                pass
        else:
            # Error
            print('Error')
            print(msg['body'])

    def send_individual_message(self):
        print(self.neighbors)
        print(self.boundjid.user)
        print("1. mostrar tabla")
        print("2. agregar vecino")
        print("3. enviar mensaje")
        opcion = input("opcion:")
        if (opcion == "3"):
            to = input("Para quien: ")
            # texto del mensaje
            mbody = input("Mensaje: ")
            for neighbor in self.neighbors:
                # mandar a todos los vecinos que no sean yo
                if (self.me != neighbor):
                    json_msg = make_msg_json(
                        origin=self.jid,
                        me=self.jid,
                        to=to,
                        msg=mbody,
                        hops=0,
                        distance=0,
                    )  # TODO: cambiar hops y distance
                    self.send_message(mto=neighbor, mbody=json_msg)









