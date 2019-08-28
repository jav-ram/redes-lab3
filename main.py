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
            distance = int(input("Distancia del nodo vecino: "))
            neighbors.append((name + "@alumchat.xyz", distance))
    return neighbors


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='XMPP client.')
    parser.add_argument('-r', dest='alg', help='Algorithm to use')
    parser.add_argument('-j', dest='jid', help='JID to use')
    parser.add_argument('-p', dest='psw', help='Password')

    args = parser.parse_args()

    if args.jid is None:
        args.jid = input('Username: ') + "@alumchat.xyz"
    if args.psw is None:
        args.psw = input('Password: ')

    cant = int(input("Cantidad de nodos vecinos: "))
    neighbors = get_neighbors(cant)
    print(neighbors)

    # if (usuario == "n"):
    #     args.jid = "ja@alumchat.xyz"
    #     args.psw = "nistal123"
    #     neighbors = [("jb@alumchat.xyz", 2), ("jc@alumchat.xyz", 7)]
    # if (usuario == "r"):
    #     args.jid = "jb@alumchat.xyz"
    #     args.psw = "rodriguez123"
    #     neighbors = [("jc@alumchat.xyz", 1), ("ja@alumchat.xyz", 2)]
    # if (usuario == "ra"):
    #     args.jid = "jc@alumchat.xyz"
    #     args.psw = "ramos123"
    #     neighbors = [("jb@alumchat.xyz", 1), ("ja@alumchat.xyz", 7)]


    if args.alg == 'flooding':
        xmpp = UserFlooding(
            jid=args.jid,
            password=args.psw,
            DEBUG=True,
            neighbors=neighbors
        )
    elif args.alg == 'dvr':
        # DVR client
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
