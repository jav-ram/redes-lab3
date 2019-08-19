import slixmpp
import sys
from threading import Thread
from slixmpp.exceptions import IqError, IqTimeout
from blessed import Terminal
import asyncio
import random
from menu import OptionsMenu
from parse import get_dict, make_msg_json, make_neighbors_list

t = Terminal()


def msg_group(msg):
    print(t.color(40)(msg))


class UserDVR(slixmpp.ClientXMPP):

    def __init__(
        self,
        jid,
        password,
        algorithm,
        DEBUG=False,
        neighbors=[],
        distance=[],
        network_size=0,
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
            self.connection,
        ))

        self.algorithm = algorithm
        self.DEBUG = DEBUG
        self.neighbors = neighbors
        self.me = jid
        self.distance = distance
        self.network_size = network_size
        self.table = {}

        # start event
        self.add_event_handler('session_start', self.start)
        # register event
        self.add_event_handler('register', self.register)
        # message event
        self.add_event_handler('message', self.message)

    def start(self, event):
        self.send_presence()
        self.get_roster()
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
                    pass
                else:
                    print(message)
            elif message_type == 'connection':
                # update neighbors
                changes = False
                nodes = message['table']
                for n in nodes:
                    if n not in self.table:
                        changes = True
                        self.table.append(n)
                    else:
                        index = self.table.index(n)
                        if n.distance < self.table[index].distance:
                            changes = True
                            self.table[index].distance = n.distance

                if changes:
                    connection_msg = make_neighbors_list(
                        self.jid,
                        self.table
                    )
                    for n in self.neighbors:
                        self.send_message(mto=n, mbody=connection_msg)

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

    def connection(self):
        # SEND AND ASK for NEIGHBORS
        # send
        table = []
        for i in range(0, len(self.neighbors)):
            table.append({
                "from": self.jid,
                "to": self.neighbors[i],
                "distance": self.distance[i],
            })
        self.table = table
        connection_msg = make_neighbors_list(
            self.jid,
            self.table
        )
        print(self.table)
        for n in self.neighbors:
            self.send_message(mto=n, mbody=connection_msg)
