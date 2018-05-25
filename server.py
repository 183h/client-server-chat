from pickle import loads, dumps

from zmq import Context, DEALER, Poller, POLLIN

class Server(object):
    def __init__(self, port):
        self._ctx = Context()

        self._socket = self._ctx.socket(DEALER)
        self._socket.bind('tcp://*:%s' % port)

        self._poller = Poller()
        self._poller.register(self._socket, POLLIN)

        self._clients = {}

        self._actions = {
            'register' : self._register_client
        }
    
    def _register_client(self, message):
            if message['pseudonym'] not in self._clients:
                self._clients[message['pseudonym']] = message['cert']
                message = {
                    'type' : 'Accepted'
                }
                
                self._send_msg(message)
            else:
                message = {
                    'type' : 'Failed'
                }
                self._send_msg(message)
        
    def _send_msg(self, message):
        pickled_message = dumps(message)
        self._socket.send(pickled_message)

        print('Sent --> ', message)
        
    def _recv_msg(self):
        pickled_message = self._socket.recv()
        received_message = loads(pickled_message)

        print("Received --> ", received_message)
        return received_message
    
    def execute(self):
        while True:
            sockets = dict(self._poller.poll())

            if sockets.get(self._socket) == POLLIN:
                received_message = self._recv_msg()

                self._actions[received_message['type']](received_message)

if __name__ == '__main__':
    s = Server(5000)
    s.execute()