import logging
from game import Game

class Tamagotchi():

    '''
    Construct a new tamagotchi with the provided parameters
    '''
    def __init__(self, health, gender, hunger, happiness, sickness):
        logging.debug(f'[Tamagotchi.__init__({health},{gender},{hunger},{happiness},{sickness})] - performing __init__')

        # use getter/Setter instead of direct assignment
        # those properties are placed only for debug purposes some will be removed, reworked or added later
        self.health = health
        self.gender = gender
        self.hunger = hunger
        self.happiness = happiness
        self.sickness = sickness

    '''
    Health setter
    '''
    def setHealth(self, h):
        if h >= 0:
            self.health = h
        else:
            raise ValueError("tamagotchi's health cannot be neggative")

    '''
    Each tick this method will be called to update the state of the tamagotchi.
    This method is responsible to apply every state modifier of the tamagotchi (eq. update the hunger)
    '''
    def update(self):
        logging.debug('[Tamagotchi.update()] - performing update')
        self.hunger = self.hunger + 0.5
        if self.hunger > 50:
            self.sickness = self.sickness + 0.5
            self.happiness = self.happiness -0.5
            if Game.isSick:
                self.health = self.health - self.sickness % 100

    '''
    Check if the tamagotchi is dead
    '''
    def isDead(self):
        # for the moment we only check the health, but later we should check sickness, hapinness, hunger, ...
        if self.health <= 0:
            return True
        return False

    '''
    Simple action, just for test purpose ... feeding, healing, and other should be implemented as this
    '''

    def aTest(self):
        print("just a simple test action to POC")

    def __str__(self):
        return f'Tamagotchi(health={self.health}, gender={self.gender}, hunger={self.hunger}, happiness={self.happiness}, sickness={self.sickness})'

    '''
       Definition of basic functions
    '''

    def activity_feeding(self):
        self.hunger = self.hunger - 1

    def activity_healing(self):
        self.health = self.health + 1