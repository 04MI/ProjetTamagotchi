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

class Server(object):
    def __init__(self, pet_data=None):
        self.pet_data = pet_data if pet_data else {}
        self.win = self.new_root = self.text = self.entry_ip = self.entry_port = None
        self.host = pet_data.get('host', '')
        self.port = pet_data.get('part', 8888)
        self.name = pet_data.get('name')
        self.address = (self.host, self.port)
        self.buffer = 1024  # Receive data sent by others, up to 1024 bytes
        self.flag = True

    def __del__(self):
        self.flag = False

    def win_init(self):
        self.win = tk.Tk()  # Create the main window
        self.win.title('Start a session')
        self.win.geometry("400x300")
        self.win.resizable(width=False, height=False)  # Immutable width, variable height, the default is True

    def win_stop(self):
        self.win.quit()
        self.win.destroy()
        return True

    def new_root_stop(self):
        for i in threading.enumerate():
            if i.name in ['client', 'start'] and i.is_alive():
                stop_thread(i.ident, SystemExit)
        self.new_root.quit()
        self.new_root.destroy()

    def win_show(self):
        # interface display
        labelIp = tk.Label(self.win, text='IP:', font=('Consolas', 18))
        labelIp.place(x=100, y=100)
        eip = tk.Variable()
        self.entry_ip = tk.Entry(self.win, textvariable=eip, font=('Consolas', 16), width=17)
        self.entry_ip.place(x=150, y=106)
        self.entry_ip.insert(0, self.host)
        labelPort = tk.Label(self.win, text='PORT:', font=('Consolas', 18))
        labelPort.place(x=75, y=150)
        e_port = tk.Variable()
        self.entry_port = tk.Entry(self.win, textvariable=e_port, font=('Consolas', 16), width=17)
        self.entry_port.place(x=150, y=155)
        self.entry_port.insert(0, self.port)
        button1 = tk.Button(self.win, text="Quit", command=self.win.quit(), font=('Consolas', 14))
        button1.place(x=290, y=200)
        button1 = tk.Button(self.win, text="Start", command=self.start_sever, font=('Consolas', 14))
        button1.place(x=220, y=200)
        button2 = tk.Button(self.win, text="Clear", command=self._clear, font=('Consolas', 14))
        button2.place(x=150, y=200)
        che = tk.Checkbutton(self.win, width=100, height=20, text='22222')
        che.place(x=180, y=300)

    def new_root_init(self):
        # Create child windows
        self.new_root = tk.Tk()
        self.new_root.withdraw()
        self.new_root.title('Start a session')
        self.new_root.geometry("400x300")
        self.new_root.resizable(width=False, height=False)  # Immutable width, variable height, the default is True

    def new_root_show(self):
        global button_root
        show_online = tk.Label(self.new_root, text='Session record', font=('Consolas', 16))
        show_online.place(x=50, y=10)
        button_root = tk.Button(self.new_root, text="Quit", command=self.new_root_stop, font=('Consolas', 14))
        button_root.place(x=250, y=9)
        self.text = tk.Text(self.new_root, height=10, width=40, font=('Consolas', 15))
        self.text.place(x=0, y=35)
        self.new_root.mainloop()

    def server(self):
        tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_server_socket.bind(self.address)
        tcp_server_socket.listen(128)

        print_str = "Server started successfully\n"
        self.text.insert(tk.INSERT, print_str)
        
        client_socket, clientAddr = tcp_server_socket.accept()
        user_name = client_socket.recv(self.buffer)
        
        print_str = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} \n {user_name.decode('utf-8')}.....successfully connected\n"
        self.text.insert(tk.INSERT, print_str)
        
        client_socket.send(user_name)

    def client(self):
        tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_client_socket.connect((self.host, int(self.port)))
        
        send_data = input("Please enter the data to send:")
        
        tcp_client_socket.send(send_data.encode("gbk"))
        recvData = tcp_client_socket.recv(self.buffer)
        
        print('The data received is:', recvData.decode('gbk'))
        tcp_client_socket.close()

    def start_sever(self):
        self.new_root.deiconify()
        self.win.withdraw()
        
        s = Thread(target=self.server, name='start', daemon=True)  # Enable a thread to start the server
        s.start()
        
        host = self.entry_ip.get()
        port = self.entry_port.get()
        if host:
            self.host = host
            PETS[self.name].update({'host': self.host})
        if port:
            self.port = port
            PETS[self.name].update({'port': int(self.port)})
        c = Thread(target=self.client, name='client', daemon=True)  # Enable a thread to start the server
        c.start()

    def _clear(self):
        self.entry_ip.delete(0, tk.END)

    def all_run(self):
        self.win_init()
        self.win_show()
        self.new_root_init()
        self.new_root_show()
        self.new_root.mainloop()
        self.win.mainloop()
