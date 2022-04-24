import logging
import time
from game import Game
import os
import json
from random import randrange

SICKNESS_MODIFIER = 0.002
SICKNESS_SCALE = 500
HAPPINESS_MODIFIER = 0.02
HAPPINESS_FEED = 1
HUNGER_MODIFIER = 0.02
HUNGER_FEED = 2
HEALTH_HEAL = 0.01
SAVE_FILENAME = 'history.json'

DAY = 30*60*60*24 

EVOLUTIONS = [
    {'name': 'bébé', 'delta':[0, DAY], 'sickness_factor':30/SICKNESS_SCALE, 'hunger_amplifier':0.02, "state":"BABY"},
    {'name': 'enfant', 'delta':[DAY, DAY*3], 'sickness_factor':10/SICKNESS_SCALE, 'hunger_amplifier':0.02, "state":"CHILD"},
    {'name': 'adulte', 'delta':[DAY*3, DAY*4], 'sickness_factor':10/SICKNESS_SCALE, 'hunger_amplifier':0.01, "state":"ADULT"},
    {'name': 'vieux', 'delta':[DAY*4, DAY*8], 'sickness_factor':30/SICKNESS_SCALE, 'hunger_amplifier':0.01, "state":"ELDER"},
]

class Tamagotchi():

    '''
    Construct a new tamagotchi with the provided parameters
    '''
    def __init__(self, name, health, gender, hunger, happiness, sickness, lifetime, friends=[]):
        logging.debug(f'[Tamagotchi.__init__({health},{gender},{hunger},{happiness},{sickness})] - performing __init__')

        self.name = name
        self.health = health
        self.gender = gender
        self.hunger = hunger
        self.happiness = happiness
        self.sickness = sickness
        self.lifetime = lifetime
        self.friends = friends

        self.updateEvolution()

    '''
    Return the current evolution stage
    '''
    def updateEvolution(self):
        for e in EVOLUTIONS:
            if self.lifetime >= e['delta'][0] and self.lifetime < e['delta'][1]:
                self.evolution = e
                break

    '''
    Health setter
    '''
    def setHealth(self, h):
        if h >= 0:
            self.health = h
        else:
            raise ValueError("tamagotchi's health cannot be neggative")

    '''
       change the situation of sickness
    '''

    def isSick(self):
        if self.sickness > 0:
            return True
        return False

    def fallSick(self):
        if randrange(SICKNESS_SCALE) < self.evolution['sickness_factor']:
            self.sickness = SICKNESS_MODIFIER

    def saveState(self):
        f=open(SAVE_FILENAME, 'w')
        f.write(self.toJSON())
        f.close()

    '''
    Each tick this method will be called to update the state of the tamagotchi.
    This method is responsible to apply every state modifier of the tamagotchi (eq. update the hunger)
    '''
    def update(self):
        logging.debug('[Tamagotchi.update()] - performing update')
        self.updateEvolution()
        self.hunger = (self.hunger + HUNGER_MODIFIER) % 100
        if self.hunger > 50:
            if not self.isSick():
                self.sickness = SICKNESS_MODIFIER
            self.happiness = self.happiness - HAPPINESS_MODIFIER
        if self.isSick():
            self.sickness = self.sickness + SICKNESS_MODIFIER
            self.health = self.health - (self.sickness * 0.01)
        self.fallSick()
        self.lifetime += 1
        self.saveState()

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
        self.hunger = self.hunger - HUNGER_FEED
        self.happiness = (self.happiness + HAPPINESS_FEED) % 100
        if self.hunger < 0:
            self.hunger = 0

    def activity_healing(self):
        self.sickness = 0

    def addFriend(self, friend):
        for f in self.friends:
            if f['name'] == friend['name']:
                return

        self.friends.append(friend)

    @staticmethod
    def fromJSON(data):
        data = json.loads(data)
        # def __init__(self, name, health, gender, hunger, happiness, sickness, lifetime, friends=[]):
        return Tamagotchi(
            data['name'],
            data['health'],
            data['gender'],
            data['hunger'],
            data['happiness'],
            data['sickness'],
            data['lifetime'],
            data['friends']
        )

    def toJSON(self):
        obj = {
            'name' : self.name,
            'health' : self.health,
            'gender' : self.gender,
            'hunger' : self.hunger,
            'happiness' : self.happiness,
            'sickness' : self.sickness,
            'lifetime' : self.lifetime,
            'friends' : self.friends
        }
        return json.dumps(obj)