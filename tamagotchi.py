import logging
from random import randrange

class Tamagotchi():

    health_Max = 50
    hunger_Max = 50
    happiness_Max = 50
    sickness_Max = 50
    gender_type = ['"male"','"female"']

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
        # not implemented yet
        pass

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