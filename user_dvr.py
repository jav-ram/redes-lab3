from my_xmpp_client import my_xmpp_client
from threading import Thread
from menu import OptionsMenu
from parse import get_dict, make_neighbors_list

class UserDVR(my_xmpp_client):

    def __init__(
        self,
        jid,
        password,
        DEBUG=False,
        neighbors=[],
        distance=[],
        network_size=0,
    ):
        super().__init__(jid, password, DEBUG, neighbors)

        """
        self.menu = Thread(target=OptionsMenu, args=(
            self.send_individual_message,
            self.connection,
        ))
        """

        self.distance = distance
        self.network_size = network_size
        self.table = {}

        # message event
        self.add_event_handler('message', self.receive_message_dvr)

    def receive_message_dvr(self, msg):
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
