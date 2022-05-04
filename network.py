from threading import Thread, Lock
import socket

class MeetServer:
    def __init__(self, ipconfig, meetCallback):
        self.host = ipconfig["ip"]
        self.port = ipconfig["port"]
        self.hasMeet = False
        self.callback = meetCallback
        pass

    def setup(self):
        pass
    
    def run(self):
        tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_server_socket.bind((self.host, self.port))
        tcp_server_socket.listen(1)

        client_socket, clientAddr = tcp_server_socket.accept()
        self.handleMeeting(client_socket)
        self.hasMeet = True
        tcp_server_socket.close()
        
    def start(self):
        self.serverThread = Thread(target=self.run)  # Enable a thread to start the server
        self.serverThread.start()
    
    def stop(self):
        print("[!] - not implemented yet !")
        pass
    
    def handleMeeting(self, client):
        print("[+] - MeetServer.handleMeeting")
        self.callback(client)
    
class MeetClient:
    def __init__(self, ipconfig, meetCallback):
        self.host = ipconfig["ip"]
        self.port = ipconfig["port"]
        self.hasMeet = False
        self.callback = meetCallback
    
    def start(self):
        tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_client_socket.connect((self.host, self.port))

        self.handleMeeting(tcp_client_socket)
        tcp_client_socket.close()
    
    def handleMeeting(self, client):
        print("[+] - MeetClient.handleMeeting - NotFullyImplemented yet")
        self.callback(client)