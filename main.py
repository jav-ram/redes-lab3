import slixmpp
import argparse
from user import User


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
    parser.add_argument('-j', dest='jid', help='JID to use')
    parser.add_argument('-p', dest='psw', help='Password')

    args = parser.parse_args()

    """
    if args.jid is None:
        #args.jid = input('Username: ')
        args.jid = "h@alumchat.xyz"
    if args.psw is None:
        #args.psw = input('Password: ')
        args.psw = "hanu"
    """
    usuario = input("Usuario: ")

    #cant = int(input("Cantidad de nodos vecinos: "))
    #neighbors = get_neighbors(cant)
    if (usuario == "n"):
        args.jid = "nistal@alumchat.xyz"
        args.psw = "nistal123"
        neighbors = [args.jid,"rodriguez@alumchat.xyz"]
    if (usuario == "r"):
        args.jid = "rodriguez@alumchat.xyz"
        args.psw = "rodriguez123"
        neighbors = [args.jid,"ramos@alumchat.xyz","nistal@alumchat.xyz"]
    if (usuario == "ra"):
        args.jid = "ramos@alumchat.xyz"
        args.psw = "ramos123"
        neighbors = [args.jid,"rodriguez@alumchat.xyz"]

    xmpp = User(
                jid=args.jid,
                password=args.psw,
                algorithm=algorithm,
                DEBUG=True,
                neighbors=neighbors
            )

    xmpp.connect()
    xmpp.process(forever=False)
