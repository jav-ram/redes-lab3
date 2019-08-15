import slixmpp
import argparse
from user import User


def algorithm():
    print("h")


def get_neighbors(cant):
    neighbors = []
    if (cant < 0):
        for i in range(0, cant):
            neighbors.append(input("Nombre del nodo vecino: "))
    return neighbors

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='XMPP client.')
    parser.add_argument('-j', dest='jid', help='JID to use')
    parser.add_argument('-p', dest='psw', help='Password')

    args = parser.parse_args()

    if args.jid is None:
        args.jid = input('Username: ')
    if args.psw is None:
        args.psw = input('Password: ')

    cant = input("Cantidad de nodos vecinos: ")
    neighbors = get_neighbors(cant)

    xmpp = User(
                jid=args.jid,
                password=args.psw,
                algorithm=algorithm,
                DEBUG=True,
                neighbors=neighbors
            )

    xmpp.register_plugin('xep_0030')  # Service Discovery
    xmpp.register_plugin('xep_0004')  # Data forms
    xmpp.register_plugin('xep_0060')  # PubSub
    xmpp.register_plugin('xep_0065')  # File transfer
    xmpp.register_plugin('xep_0199')  # XMPP Ping
    xmpp.register_plugin('xep_0047')  # In-band Bytestreams
    xmpp.register_plugin('xep_0066')  # Out-of-band Data
    xmpp.register_plugin('xep_0077')  # Register
    xmpp.register_plugin('xep_0065')  # SOCKS5 Bytestreams

    xmpp.plugin['xep_0077'].force_registration = True

    xmpp.connect()
    xmpp.process(forever=False)
