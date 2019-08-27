import slixmpp
import time
from threading import Thread
from slixmpp.exceptions import IqError, IqTimeout
from parse import make_msg_json


class my_xmpp_client(slixmpp.ClientXMPP):
    def __init__(
        self,
        jid,
        password,
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

        self.menu = Thread(target=self.handle_menu)

        self.DEBUG = DEBUG
        self.neighbors = neighbors

        # start event
        self.add_event_handler('session_start', self.start)
        # register event
        self.add_event_handler('register', self.register)

    def start(self, event):
        self.send_presence()
        self.get_roster()
        print(self.jid)
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
    
    def send_individual_message(self, neighbor, message, hops, origin):
        print("enviando mensaje", neighbor[0], neighbor[1])
        time.sleep(neighbor[1])
        print("mensaje enviado", neighbor[0], neighbor[1])
        json_msg = make_msg_json(
            origin=origin,
            me=self.jid,
            to=neighbor[0],
            msg=message,
            hops=hops,
            distance=neighbor[1],
        )
        self.send_message(mto=neighbor[0], mbody=json_msg)

    def handle_menu(self):
        print(self.neighbors)
        print(self.jid)
        print("1. agregar vecino")
        print("2. enviar mensaje")
        opcion = input("opcion:")
        if (opcion == "1"):
            name = input("Nombre del nodo vecino: ")
            distance = input("Distancia del nodo vecino: ")
            self.neighbors.append((name, distance))
        if (opcion == "2"):
            to = input("Para quien: ")
            # texto del mensaje
            mbody = input("Mensaje: ")
            for neighbor in self.neighbors:
                # mandar a todos los vecinos que no sean yo
                if (self.jid != neighbor[0]):
                    self.send_individual_message(neighbor, mbody, 50, self.jid)
                    