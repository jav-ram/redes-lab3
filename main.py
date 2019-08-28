import slixmpp
import argparse
from user_flooding import UserFlooding
from user_dvr import UserDVR
from user_lsr import UserLSR


def algorithm():
    print("h")


def get_neighbors(cant):
    neighbors = []
    if (cant > 0):
        for i in range(0, cant):
            name = input("Nombre del nodo vecino: ")
            distance = input("Distancia del nodo vecino: ")
            neighbors.append((name, distance))
    return neighbors


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='XMPP client.')
    parser.add_argument('-r', dest='alg', help='Algorithm to use')
    parser.add_argument('-j', dest='jid', help='JID to use')
    parser.add_argument('-p', dest='psw', help='Password')

    args = parser.parse_args()

    usuario = input("Usuario: ")

    # cant = int(input("Cantidad de nodos vecinos: "))
    # neighbors = get_neighbors(cant)
    if (usuario == "n"):
        args.jid = "nistal@alumchat.xyz"
        args.psw = "nistal123"
        neighbors = [("ramos@alumchat.xyz", 7)]
    if (usuario == "r"):
        args.jid = "rodriguez@alumchat.xyz"
        args.psw = "rodriguez123"
        neighbors = [("ramos@alumchat.xyz", 1)]
    if (usuario == "ra"):
        args.jid = "ramos@alumchat.xyz"
        args.psw = "ramos123"
        neighbors = [("rodriguez@alumchat.xyz", 1), ("nistal@alumchat.xyz", 7)]

    """ if args.jid is None:
        args.jid = input('Username: ')
    if args.psw is None:
        args.psw = input('Password: ') """

    if args.alg == 'flooding':
        xmpp = UserFlooding(
            jid=args.jid,
            password=args.psw,
            DEBUG=True,
            neighbors=neighbors
        )
    elif args.alg == 'dvr':
        # DVR client
        network_size = input("Tamaño de la red: ")
        xmpp = UserDVR(
            jid=args.jid,
            password=args.psw,
            DEBUG=True,
            neighbors=neighbors,
        )
    elif args.alg == 'lsr':
        # LSR client
        xmpp = UserLSR(
            jid=args.jid,
            password=args.psw,
            DEBUG=True,
            neighbors=neighbors
        )

    xmpp.connect()
    xmpp.process(forever=False)
