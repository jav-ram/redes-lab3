from my_xmpp_client import my_xmpp_client
from threading import Thread
from menu import OptionsMenu
from parse import get_dict, make_neighbors_list, make_msg_json
from graph import Graph, dijsktra

INFINIT = 100000


class UserDVR(my_xmpp_client):

    def __init__(
        self,
        jid,
        password,
        DEBUG=False,
        neighbors=[],
        network_size=0,
    ):
        super().__init__(jid, password, DEBUG, neighbors)
        self.menu = Thread(target=OptionsMenu, args=(
            self.send_message_custom,
            self.connection,
        ))

        self.network_size = network_size
        self.table = {
            self.jid: neighbors
        }

        # message event
        self.add_event_handler('message', self.receive_message_dvr)

    def receive_message_dvr(self, msg):
        if msg['type'] in ('normal', 'chat'):
            # parceo string to json
            message = get_dict(msg["body"])
            message_type = message['type']
            message_from = message['from']

            if message_type == 'message':
                message_to = message['to']
                if message['to'] != self.jid:
                    closest = self.get_closest(message_to)
                    print('--------------------------------------------')
                    print(closest)
                    print('--------------------------------------------')
                    # send message
                    self.send_individual_message(
                        message_to,
                        message['msg'],
                        message['hops'] + 1,
                        message['origin'],
                        closest['path'],
                        closest['distance'] + message['distance']
                    )

                else:
                    print(message)
            elif message_type == 'connection':
                # update neighbors
                changes = False
                nodes = message['table']
                for n in nodes:
                    if n not in self.table:
                        changes = True
                        self.table[message_from] = nodes[n]
                    elif len(nodes[n]) > len(self.table[n]):
                        changes = True
                        self.table[message_from] = nodes[n]

                # fill empties
                for node in self.table:
                    if node != self.jid:
                        i = 0
                        for their_neighbor in self.table[node]:
                            for my_neighbor in self.table[self.jid]:
                                if their_neighbor[0] == my_neighbor[0]:
                                    i = i + 1

                            if i == 0 and their_neighbor[0] != self.jid:
                                changes = True
                                self.table[self.jid].append(
                                    (their_neighbor[0], None)
                                )

                # fill distance
                # generate graph
                # (nodeA, nodeB, distance)
                graph = Graph()
                edges = []
                for node in self.table:
                    for connection in self.table[node]:
                        if connection[1] is not None:
                            edges.append((node, connection[0], connection[1]))

                for edge in edges:
                    graph.add_edge(*edge)

                # apply to everyone
                for index, neighbor in enumerate(self.table[self.jid]):
                    name = neighbor[0]
                    path = dijsktra(graph, self.jid, name)
                    distance = 0
                    for i in range(1, len(path)):
                        previus = self.table[path[i - 1]]
                        for p in previus:
                            if p[0] == path[i]:
                                distance = distance + p[1]
                    if distance < neighbor[1]:
                        self.table[self.jid][index] = (path[i], distance)

                if True:
                    connection_msg = make(
                        self.jid,
                        self.table
                    )
                    for n in self.neighbors:
                        self.send_message(mto=n[0], mbody=connection_msg)
        else:
            # Error
            print('Error')
            print(msg['body'])

    def get_closest(self, target):
        print(self.table)
        # is neighbor
        # get closest neighbor
        options = []
        for node in self.table:
            # find
            for n in self.table[node]:
                if n[0] == target:
                    options.append({
                        'path': node,
                        'distance': n[1]
                    })

        closest = {
            'path': "",
            'distance': 100000,
        }

        print("Options")
        for o in options:
            if o["distance"] < closest["distance"]:
                closest = o

        print(options)
        print(closest)

        if closest['path'] == self.jid:
            closest = {
                'path': target,
                'distance': 0,
            }

        print(closest)

        return closest

    def send_message_custom(self):
        to = input("to: ")
        msg = input("mensaje: ")

        closest = self.get_closest(to)
        print(closest)

        self.send_individual_message(
            to,
            msg,
            1,
            self.jid,
            closest['path'],
            closest['distance']
        )

    def connection(self):
        # SEND AND ASK for NEIGHBORS
        # sen   d
        connection_msg = make_neighbors_list(
            self.jid,
            self.table
        )
        for n in self.neighbors:
            self.send_message(mto=n[0], mbody=connection_msg)
