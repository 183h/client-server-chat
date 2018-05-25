from pickle import loads, dumps

from zmq import Context, DEALER

class Client(object):
    def __init__(self):
        self._ctx = Context()

        self._socket = self._ctx.socket(DEALER)

        self._server_port = None

        self._actions = {
            'actions' : self._list_actions,
            'exit' : self._exit,
            'register' : self._register,
        }

    def _list_actions(self):
        print(
            '''
            Available actions:
                actions : list available actions,
                register : register client to server,
                exit : terminate client
            '''
        )

    def _exit(self):
        exit()
    
    def _send_msg(self, message):
        pickled_message = dumps(message)
        self._socket.send(pickled_message)
        
    def _recv_msg(self):
        pickled_message = self._socket.recv()
        received_message = loads(pickled_message)

        return received_message
    
    def _register(self):
        pseudonym = input('Enter pseudonym --> ')
        cert = input('Enter certificate --> ')

        message = {
            'type' : 'register',
            'pseudonym' : pseudonym,
            'cert' : cert
        }

        self._send_msg(message)
        response = self._recv_msg()

        print(response)

    def execute(self):
        self._server_port = input('Enter server port --> ')
        self._socket.connect('tcp://localhost:%s' % self._server_port)

        print('For available actions use keyword actions.')
        while True:
            i = input('Define action --> ')

            if i in self._actions: 
                self._actions[i]()
            else:
                print('Undefined action!')
            

if __name__ == '__main__':
    c = Client()
    c.execute()