from my_xmpp_client import my_xmpp_client
from threading import Thread
from parse import get_dict

class UserFlooding(my_xmpp_client):
    
    def __init__(
        self,
        jid,
        password,
        DEBUG=False,
        neighbors=[],
    ):
        super().__init__(jid, password, DEBUG, neighbors)
        # message event
        self.add_event_handler('message', self.receive_message_flooding)

    def receive_message_flooding(self, msg):
        if msg['type'] in ('normal', 'chat'):
            # parceo string to json
            print(msg["body"])
            print(self.neighbors)
            message = get_dict(msg["body"])
            message_type = message['type']
            if message_type == 'message':
                if message['to'] != self.jid:
                    for neighbor in self.neighbors:
                        # enviar a todos los vecinos que no sean el origen, que no sea el vecino que mando el ultimo menasje y que no sea el vecino que creo el mensaje
                        print(neighbor[0])
                        print(message['from'])
                        print(message['origin'])
                        print(message['hops'])
                        print("****")
                        
                        if (
                            message['from'] != neighbor[0] and
                            message['origin'] != neighbor[0] and 
                            message['hops'] != 0
                        ):
                            self.send_individual_message(message['to'],message["msg"],message['hops']-1,message['origin'],neighbor)
                        
                else:
                    print(message)
        else:
            # Error
            print('Error')
            print(msg['body'])

    def handle_flooding_table(self):
        return