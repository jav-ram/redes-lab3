import slixmpp
from threading import Thread
from slixmpp.exceptions import IqError, IqTimeout
from menu import OptionsMenu, get_option, menu
from blessed import Terminal
import asyncio
import random

t = Terminal()

possible_status = [
    'dnd',
    'chat',
    'xa',
    'away',
]


def msg_group(msg):
    print(t.color(40)(msg))


class User(slixmpp.ClientXMPP):

    def __init__(self, jid, password):
        super().__init__(jid, password)

        self.menu = Thread(target=OptionsMenu, args=(
            menu,
            self.send_individual_message,
            self.get_roster_print,
            self.send_file,
            self.add_to_roster,
            self.delete_account,
            self.change_status,
            self.get_one_user,
            self.exit,
        ))

        # start event
        self.add_event_handler('session_start', self.start)
        # register event
        self.add_event_handler('register', self.register)
        # message event
        self.add_event_handler('message', self.message)
        # group message event
        self.add_event_handler("groupchat_message", self.muc_message)

    def start(self, event):
        # <presence />
        self.send_presence()
        # <iq type=get>
        #   <query xmlns="data:iq:rooster" />
        # </iq>
        self.get_roster()
        print(self.boundjid)
        # self.send_message(mto='a@alumchat.xyz', mbody='Hello')
        self.menu.start()

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

    def delete_account(self):
        asyncio.run(self.delete_account_send())

    async def delete_account_send(self):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['from'] = self.boundjid.jid
        resp['register'] = ' '
        resp['register']['remove'] = ' '

        try:
            await resp.send()
            print('')
        except IqError:
            print("Error al eliminar cuenta")
        except IqTimeout:
            print("timeout")
            self.disconnect()

    def message(self, msg):
        if msg['type'] in ('normal', 'chat'):
            # Do something
            print( t.color(random.randint(9, 15))(t.bold(str(msg['from'])) + ': ' + str(msg['body'])))
        else:
            # Error
            print('Error')
            print(msg['body'])

    def muc_message(self, msg):
        if msg['type'] in ('normal', 'chat'):
            # Do something
            msg_group(msg['body'])
        else:
            # Error
            print('Error')
            print(msg['body'])

    def send_individual_message(self):
        mto = get_option('Para: ')
        mbody = get_option('Contenido: ')
        self.send_message(mto=mto, mbody=mbody)

    # TODO: enter to room
    def send_group_message(self):
        pass

    def get_my_roster(self):
        print(self.client_roster)
        print(self.get_roster())

    def change_status(self):
        status = get_option('Nuevo status: ')
        while status not in possible_status:
            status = get_option('Nuevo status: ')

        self.make_presence(pshow=status)

    def get_roster_print(self):
        for jid in self.roster[self.jid]:
            print(jid)
            print(self.roster[self.jid][jid])
            print('--------------------------')

    def get_one_user(self):
        jid = get_option('jid: ')
        print(self.roster[self.jid][jid])

    def add_to_roster(self):
        jid = get_option('jid: ')
        self.send_presence_subscription(pto=jid)

    def exit(self):
        self.disconnect()

    def send_file(self):
        asyncio.run(self.send_file_async())

    async def send_file_async(self):

        file_name = 'README.md'
        receiver = get_option('Para: ')

        stream = await self['xep_0047'].open_stream(receiver)

        with open(file_name) as f:
            data = f.read()
            stream.sendall(data)








