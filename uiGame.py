import ctypes
import threading
import inspect
from game import Game
from threading import Thread, Lock
import tkinter as tk
from time import sleep
from utils import Action, Actions
from tkinter import messagebox, simpledialog
from tamagotchi import *
import socket

PETS = {}


class UiGame(Game):
    def __init__(self, tickrate, tamagotchi):
        Game.__init__(self, tickrate, tamagotchi)
        self.rows = 1
        self.root = tk.Tk()
        self.root.title('Tamagotchi')
        self.root.geometry('300x300')

        self.canvas = tk.Canvas(self.root)
        self.canvas.pack()
        self.text = tk.Text(self.root, width=67, height=35)  # raw data entry box
        self.text.pack()

        # s = tk.StringVar()

        # l = tk.Label(root, textvariable=s, font="Consolas")
        # l.grid(columnspan=3, column=0, row=1)
        # s.set('lolmdr')
        self.stringVars = {
            'health': tk.StringVar(),
            'hunger': tk.StringVar(),
            'happiness': tk.StringVar(),
            'sickness': tk.StringVar()
        }

        # rows = 1
        for k in self.stringVars.keys():
            l = tk.Label(self.canvas, textvariable=self.stringVars[k], font="Consolas")
            l.grid(columnspan=3, column=0, row=self.rows)
            self.rows += 1

        # b = tk.Button(root, text="lol", command=lambda:fizz())
        # b.grid(column=1, row=1)
        for a in self.actions.actions:
            b = tk.Button(self.canvas, text=a.trigger, command=lambda trigger=a.trigger: self.handleAction(trigger))
            b.grid(column=1, row=self.rows)
            self.rows += 1

    '''
    Feed the differents passible action of the game
    '''

    def feedActions(self):
        self.actions.addAction(Action('FEED', self.tamagotchi.activity_feeding, 'Action for test purpose'))
        self.actions.addAction(Action('HEAL', self.tamagotchi.activity_healing, 'Action for test purpose'))
        self.actions.addAction(Action('KILL', self.killTamagotchi, "Kill the tamagotchi"))

    def updateView(self):
        if self.tamagotchi.isDead() and len(self.canvas.winfo_children()) > 1:
            for c in self.canvas.winfo_children():
                c.destroy()
            l = tk.Label(self.canvas, text="your tamagotchi is dead :'(", font="Consolas")
            l.grid(columnspan=3, column=0, row=1)
            pass

        for k in self.stringVars.keys():
            v = getattr(self.tamagotchi, k)
            self.stringVars[k].set('%s : %s' % (k, (v)))

    # TODO : a modifier pour utiliser tkinter
    def _run(self, mutex):
        while True:
            if self.isEnded():
                self.updateView()
                break

            # we use mutex to avoid race condition or any problem with concurrency
            mutex.acquire()
            self.tick()
            mutex.release()
            self.updateView()
            sleep(1 / self.tickrate)

    def run(self):
        self.mutex = Lock()
        t_tick = Thread(target=self._run, args=[self.mutex])
        t_tick.start()

        self.root.mainloop()


class UiMenu(UiGame):
    def __init__(self, tickrate, tamagotchi):
        UiGame.__init__(self, tickrate, tamagotchi)
        self.menubar = tk.Menu(self.root)
        self.old_tamagotchi = self.tamagotchi
        self.meeting_button = None
        self.add_new_pet_button = None
        self.server = None

    """
    At the beginning of the game, there are two options
         1. Create a new game
         2. Load an existing archive
    """

    def check_need(self):
        return tk.messagebox.askyesno(title='system_hint', message='Need to create a new game?')  # Return'True','False'

    def create_new_game(self):
        """
        To start a new game, the Tamagotchi name must be entered
        """
        var_box = self.check_need()
        if var_box:
            print("Start creating a new game")
            var_string = simpledialog.askstring(title="", prompt="Enter the name of the tamagotchi:")
            if not var_string:
                self.create_new_game()
            else:
                pet = {'name': var_string, 'health': 100, 'gender': 'male', 'hunger': 0, 'happiness': 100,
                       'sickness': 0, 'lifetime': 0, 'host': '127.0.0.1', 'part': 8888}
                PETS.update({var_string: pet})
                self.add_new_pet(pet)
                self.meeting(var_string)
                self.tamagotchi = Tamagotchi(health=pet.get('health'), gender=pet.get('gender'),
                                             hunger=pet.get('hunger'), happiness=pet.get('happiness'),
                                             sickness=pet.get('sickness'), lifetime=pet.get('lifetime'))
                self.run()

    def use_history_data(self):
        self.tamagotchi = self.old_tamagotchi
        self.run()

    def meeting(self, pet_name):
        """
        First menu: start a session
            Pick a random port and opens a TCP socket on it, and wait for someone to connect to it,
            once someone connects, they send messages to each other, then it closes the socket and returns to the main menu
        """
        if not self.server or not self.server.flag:
            self.server = Server(pet_data=PETS[pet_name])
        if not self.meeting_button:
            meet = Action('MEET', self.killTamagotchi, "Start a session")
            self.meeting_button = tk.Button(self.canvas, text=meet.trigger, command=self.server.all_run)
        self.meeting_button.grid(column=1, row=self.rows)
        self.rows += 1

    def add_new_pet(self, pet):
        """
        Second menu: add another pet
            Ask for the ip and port to join, try to add him,
            exchange information and go back to the menu
        """
        if not self.server or not self.server.flag:
            self.server = Server(pet_data=pet)
        if not self.add_new_pet_button:
            add = Action('ADD', self.killTamagotchi, "Add another Tamagotchi")
            self.add_new_pet_button = tk.Button(self.canvas, text=add.trigger, command=self.server.all_run)
        self.add_new_pet_button.grid(column=1, row=self.rows)
        self.rows += 1

    def add_command(self):
        self.menubar.add_command(label="Create new game", command=self.create_new_game)
        self.menubar.add_command(label="Load an existing archive", command=self.use_history_data)
        self.menubar.add_command(label="Quit", command=self.root.destroy)

    def main(self):
        self.add_command()
        self.root.config(menu=self.menubar)
        self.root.mainloop()


def stop_thread(tid, exctype) -> bool:
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    return True


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
