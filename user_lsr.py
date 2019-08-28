import slixmpp
import networkx as nx
import matplotlib.pyplot as plt
import sys
from threading import Thread
from slixmpp.exceptions import IqError, IqTimeout
from blessed import Terminal
import asyncio
import random
import time
import json
from menu import OptionsMenu
from parse import get_dict, make_msg_json, make_neighbors_list, make_connection_json


class UserLSR(slixmpp.ClientXMPP):

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

        self.menu = Thread(target=OptionsMenu, args=(
            self.send_individual_message,
            self.show_graph,
        ))

        self.DEBUG = DEBUG
        self.neighbors = neighbors
        self.me = jid
        self.table = {}
        self.graph = nx.Graph()

        # start event
        self.add_event_handler('session_start', self.start)
        # register event
        self.add_event_handler('register', self.register)
        # message event
        self.add_event_handler('message', self.message)

    def send_neighbors(self):
        for neighbor, distance in self.neighbors:
            time.sleep(3)
            connection_msg = make_neighbors_list(
                self.jid, self.neighbors, hops=1)
            self.send_message(mto=neighbor, mbody=connection_msg)

    def send_message_to_neighbor(self, neighbor, mbody):
        self.send_message(mto=neighbor, mbody=connection_msg)

    def start(self, event):
        self.send_presence()
        self.get_roster()
        self.send_neighbors()
        self.menu.start()  # Start while

    async def register(self, iq):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password

        try:
            await resp.send()
            print('Account created')
        except IqError:
            print('Error al crear cuenta, probablemente ya existe')
        except IqTimeout:
            print('timeout')
            self.disconnect()

    def message(self, msg):
        if msg['type'] in ('normal', 'chat'):
            # parceo string to json
            message = get_dict(msg['body'])
            message_type = message['type']
            sender = message['from']
            hops = message['hops']

            if message_type == 'message':
                to = message['to']
                if to == self.jid:
                    print("Message Recieved: ", message)
                else:
                    s_path = nx.shortest_path(self.graph, self.jid, to)
                    message['hops'] = hops + 1
                    message['from'] = self.jid
                    message['distance'] = message['distance'] + \
                        self.get_neighbor_distance(s_path[1])
                    self.send_message(mto=s_path[1], mbody=json.dumps(message))

            elif message_type == 'connection':
                table = message['table']
                if sender in list(map(lambda x: x[0], self.neighbors)):
                    hops = 1
                if not self.has_same_table_entry(sender, table, hops):
                    self.add_table_entry(sender, table, hops)
                    print(self.table)
                    for neighbor, distance in self.neighbors:
                        if sender != neighbor:
                            connection_msg = make_neighbors_list(
                                sender, table, hops=message['hops'] + 1)
                            self.send_message(
                                mto=neighbor, mbody=connection_msg)
                    self.send_neighbors()

            elif message_type == 'response':
                pass
        else:
            # Error
            print('Error')
            print(msg['body'])

    def add_table_entry(self, node_jid, neighbors, distance):
        self.table[node_jid] = {
            'neighbors': neighbors, 'hops': distance}
        new_graph = nx.Graph()
        for key, value in self.table.items():
            for neighbor in value['neighbors']:
                new_graph.add_edge(key, neighbor[0], weight=neighbor[1])
        self.graph = new_graph

    def has_same_table_entry(self, node_jid, neighbors, distance):
        if node_jid in list(self.table.keys()):
            entry = self.table[node_jid]
            if entry['neighbors'] == neighbors and distance <= entry['hops']:
                return True

        return False

    def show_graph(self):
        nx.draw(self.graph, with_labels=True)
        plt.show()

    def get_neighbor_distance(self, neighbor):
        index = list(map(lambda x: x[0], self.neighbors)).index(neighbor)
        return self.neighbors[index][1]

    def send_individual_message(self):
        to = input('Para quien: ')
        mbody = input('Mensaje: ')
        s_path = nx.shortest_path(self.graph, self.jid, to)
        json_msg = make_msg_json(
            origin=self.jid,
            me=self.jid,
            to=to,
            msg=mbody,
            hops=1,
            distance=self.get_neighbor_distance(s_path[1]),
        )
        self.send_message(mto=s_path[1], mbody=json_msg)
