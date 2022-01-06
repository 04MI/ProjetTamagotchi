import logging
from threading import Thread, Lock
from time import sleep
from utils import Action, Actions

class Game():

    '''
    Initiate a new Game Object
    '''
    def __init__(self, tickrate, tamagotchi):
        self.tickrate = tickrate
        self.tamagotchi = tamagotchi
        self.quit = False

        self.actions = Actions()
        self.feedActions()

    '''
    Feed the differents passible action of the game
    '''
    def feedActions(self):
        self.actions.addAction(Action('S', self.displayStatus, "Get the current status of the tamagotchi"))
        self.actions.addAction(Action('T', self.tamagotchi.aTest, 'action for test purpose'))
        self.actions.addAction(Action('Q', self.quitGame, "Quit"))

    '''
    Perform a tick of the game
    '''
    def tick(self):
        logging.debug('[Game.tick()] - performing tick')
        self.tamagotchi.update()

    '''
    Method that will run in background to update the tamagotchi at each tick
    '''
    def _run(self, mutex):
        while True:
            if self.quit :
                break

            # we use mutex to avoid race condition or any problem with concurrency
            mutex.acquire()
            self.tick()
            mutex.release()
            
            sleep(1/self.tickrate)

    '''
    Display the status of the tamagotchi
    '''
    def displayStatus(self):
        status = f'tamagotchi: {self.tamagotchi}\n'
        print(status)

    '''
    Display the game menu
    '''
    def displayMenu(self):
        self.displayStatus()
        menu = ""

        for a in self.actions.actions:
            menu += f'\t{a.trigger} - {a.description}\n'

        print(menu)

    '''
    Set the flag to quit the game
    '''
    def quitGame(self):
        self.quit = True

    '''
    Run a single game
    '''
    def run(self):
        mutex = Lock()
        t_tick = Thread(target=self._run, args=[mutex])
        t_tick.start()

        while True:
            if self.quit:
                break

            self.displayMenu()
            choice = input('> ')
            choice = choice.upper()

            if not self.actions.isPresent(choice):
                print(f'action:  {choice} not recognized as a valid action')
            else:
                mutex.acquire()
                self.actions.getHandler(choice)()
                mutex.release()

        t_tick.join()