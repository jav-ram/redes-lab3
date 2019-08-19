import slixmpp
import argparse
from user import User
from user_dvr import UserDVR


def algorithm():
    print("h")


def get_neighbors(cant):
    neighbors = []
    if (cant > 0):
        for i in range(0, cant):
            neighbors.append(input("Nombre del nodo vecino: "))
    return neighbors

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='XMPP client.')
    parser.add_argument('-r', dest='alg', help='Algorithm to use')
    parser.add_argument('-j', dest='jid', help='JID to use')
    parser.add_argument('-p', dest='psw', help='Password')

    args = parser.parse_args()

    usuario = input("Usuario: ")
    network_size = input("Tamaño de la red: ")

    # cant = int(input("Cantidad de nodos vecinos: "))
    # neighbors = get_neighbors(cant)
    if (usuario == "n"):
        args.jid = "nistal@alumchat.xyz"
        args.psw = "nistal123"
        neighbors = ["rodriguez@alumchat.xyz", "ramos@alumchat.xyz"]
        distance = [2, 7]
    if (usuario == "r"):
        args.jid = "rodriguez@alumchat.xyz"
        args.psw = "rodriguez123"
        neighbors = ["ramos@alumchat.xyz", "nistal@alumchat.xyz"]
        distance = [1, 2]
    if (usuario == "ra"):
        args.jid = "ramos@alumchat.xyz"
        args.psw = "ramos123"
        neighbors = ["rodriguez@alumchat.xyz", "nistal@alumchat.xyz"]
        distance = [1, 7]

    """ if args.jid is None:
        args.jid = input('Username: ')
    if args.psw is None:
        args.psw = input('Password: ') """

    if args.alg == 'flooding':
        xmpp = User(
                    jid=args.jid,
                    password=args.psw,
                    algorithm=algorithm,
                    DEBUG=True,
                    neighbors=neighbors
                )
    elif args.alg == 'dvr':
        # DVR client
        print(distance)
        xmpp = UserDVR(
                    jid=args.jid,
                    password=args.psw,
                    algorithm=algorithm,
                    DEBUG=True,
                    neighbors=neighbors,
                    distance=distance,
                )
    elif args.alg == '':
        # OTRO
        pass

    xmpp.connect()
    xmpp.process(forever=False)
