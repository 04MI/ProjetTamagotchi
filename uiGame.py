from game import Game
from threading import Thread, Lock
import tkinter as tk
from time import sleep
from utils import Action, Actions

class UiGame(Game):
    def __init__(self, tickrate, tamagotchi):
        Game.__init__(self, tickrate, tamagotchi)
        self.root = tk.Tk()
        self.root.title('Tamagotchi')
        self.root.geometry('300x300')

        self.canvas = tk.Canvas(self.root)
        self.canvas.pack()

        # s = tk.StringVar()
        # l = tk.Label(root, textvariable=s, font="Consolas")
        # l.grid(columnspan=3, column=0, row=1)
        # s.set('lolmdr')
        self.stringVars = {
            'health' : tk.StringVar(),
            'hunger' : tk.StringVar(),
            'happiness' : tk.StringVar(),
            'sickness' : tk.StringVar()
        }


        rows = 1
        for k in self.stringVars.keys():
            l = tk.Label(self.canvas, textvariable=self.stringVars[k], font="Consolas")
            l.grid(columnspan=3, column=0, row=rows)
            rows += 1

        # b = tk.Button(root, text="lol", command=lambda:fizz())
        # b.grid(column=1, row=1)
        for a in self.actions.actions:
            b = tk.Button(self.canvas, text=a.trigger, command=lambda trigger=a.trigger:self.handleAction(trigger))
            b.grid(column=1, row=rows)
            rows += 1

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