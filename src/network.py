from threading import Thread, Lock
import socket

class MeetServer:
    '''
    Class used as server for meeting, is responsible to start the server, and forward incomming client to a predefined callback function.
    '''

    def __init__(self, ipconfig, meetCallback):
        '''Initialize a new MeetServer with a specified ip to listen to, and a callback function that will be called, when a client is connected.

        :param ipconfig: tuple specifying ip, and port to listen to.
        :param meetCallback: function to call when a client is connected, the client socket will be given to that function.
        '''
        self.host = ipconfig["ip"]
        self.port = ipconfig["port"]
        self.hasMeet = False
        self.callback = meetCallback

    def setup(self):
        '''
        Not implemented yet.
        '''
        pass
    
    def run(self):
        '''
        Method that start the listenning socket, and wait for a client to connect to.
        '''
        
        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server_socket.bind((self.host, self.port))
        self.tcp_server_socket.listen(1)

        client_socket, _ = self.tcp_server_socket.accept()
        self.handleMeeting(client_socket)
        self.hasMeet = True
        
        
    def start(self):
        '''
        Method that start a thread that will handle the incomming client.
        '''
        self.serverThread = Thread(target=self.run)
        self.serverThread.start()
    
    def stop(self):
        '''
        Close the listenning socket.
        '''
        self.tcp_server_socket.close()
    
    def handleMeeting(self, client):
        '''
        Forward the incomming client to the callback method.
        '''
        self.callback(client)
    
class MeetClient:
    '''
    Class used as client for meeting, is responsible to connect to the meeting server, and forward incomming connection to a predefined callback function.
    '''

    def __init__(self, ipconfig, meetCallback):
        '''Initialize a new MeetServer with a specified ip to connect to, and a callback function that will be called when connected.

        :param ipconfig: tuple specifying ip, and port to connect to.
        :param meetCallback: function to call when connected, the server socket will be given to that function.
        '''
        self.host = ipconfig["ip"]
        self.port = ipconfig["port"]
        self.hasMeet = False
        self.callback = meetCallback
    
    def start(self):
        '''
        Try to connect to the specified server and when connected call the meeting handler.
        '''
        tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_client_socket.connect((self.host, self.port))

        self.handleMeeting(tcp_client_socket)
    
    def handleMeeting(self, client):
        '''
        Forward the connection to the callback method.
        '''
        self.callback(client)