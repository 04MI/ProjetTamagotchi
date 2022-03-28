from game import Game
from dino import *
from threading import Thread, Lock
import tkinter as tk
from time import sleep
from utils import Action, Actions

class UiGame(Game,DinoGame):
    def __init__(self, tickrate, tamagotchi):
        Game.__init__(self, tickrate, tamagotchi)
        DinoGame.__init__(self)

        self.title('Tamagotchi')
        self.geometry('300x300')

        self.canvas = Canvas(self)
        self.canvas.pack()

    def Tamagotchi_window(self):
        # s = StringVar()
        # l = Label(root, textvariable=s, font="Consolas")
        # l.grid(columnspan=3, column=0, row=1)
        # s.set('lolmdr')
        self.stringVars = {
            'health' : StringVar(),
            'hunger' : StringVar(),
            'happiness' : StringVar(),
            'sickness' : StringVar()
        }


        rows = 1
        for k in self.stringVars.keys():
            l = Label(self.canvas, textvariable=self.stringVars[k], font="Consolas")
            l.grid(columnspan=3, column=0, row=rows)
            rows += 1

        # b = Button(root, text="lol", command=lambda:fizz())
        # b.grid(column=1, row=1)
        for a in self.actions.actions:
            b = Button(self.canvas, text=a.trigger, command=lambda trigger=a.trigger:self.handleAction(trigger))
            b.grid(column=1, row=rows)
            rows += 1

    '''
    Feed the differents passible action of the game
    '''
    def feedActions(self):
        self.actions.addAction(Action('FEED', self.tamagotchi.activity_feeding, 'Action for test purpose'))
        self.actions.addAction(Action('HEAL', self.tamagotchi.activity_healing, 'Action for test purpose'))
        self.actions.addAction(Action('KILL', self.killTamagotchi, "Kill the tamagotchi"))
        self.actions.addAction(Action('DINO',self.Dino , "Dino game starts."))
    #lambda x:self.Dino(self)
    def Dino(self):

        self.dinoStart=True
        self.after_cancel(self.ani)
        self.canvas.destroy()
        self.bind('<Escape>',lambda x:self.Back_Run())#bind p to pause
        self.Start()
    def Back_Run(self):
        self.canvas.destroy()
        self.geometry('300x300')
        self.dinoStart=False
        self.canvas = Canvas(self)
        self.canvas.pack()
        self.run()

    def updateView(self):
        if self.tamagotchi.isDead() and len(self.canvas.winfo_children()) > 1:
            for c in self.canvas.winfo_children():
                c.destroy()
            l = Label(self.canvas, text="your tamagotchi is dead :'(", font="Consolas")
            l.grid(columnspan=3, column=0, row=1)
            pass

        for k in self.stringVars.keys():
            v = getattr(self.tamagotchi, k)
            self.stringVars[k].set('%s : %s' % (k, (v)))


    # TODO : a modifier pour utiliser tkinter
    def _run(self):
        if self.isEnded():
            self.updateView()
            self.after_cancel(self.ani)
            return

        # we use mutex to avoid race condition or any problem with concurrency
        self.mutex.acquire()
        self.tick()
        self.mutex.release()
        self.updateView()
        self.ani=self.after(int(1000*1 / self.tickrate),self._run)
        #sleep(1 / self.tickrate)

    def run(self):
        #global t_tick
        self.Tamagotchi_window()
        self.mutex = Lock()
        self._run()
        #t_tick = Thread(target=self._run, args=[self.mutex])
        #t_tick.daemon=True
        #t_tick.start()


        self.mainloop()