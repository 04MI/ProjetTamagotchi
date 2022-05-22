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
    Class that represent a Tamagotchi.
    '''

    def __init__(self, name, health, gender, hunger, happiness, sickness, lifetime, friends=[], scores=[]):
        '''__init__(self, name, health, gender, hunger, happiness, sickness, lifetime, friends=[], scores=[])
        Instanciate a new tamagotchi using the provided parameters as caracteristics.
        '''

        logging.debug(f'[Tamagotchi.__init__({health},{gender},{hunger},{happiness},{sickness})] - performing __init__')

        self.name = name
        self.health = health
        self.gender = gender
        self.hunger = hunger
        self.happiness = happiness
        self.sickness = sickness
        self.lifetime = lifetime
        self.friends = friends
        self.scores = scores

        self.updateEvolution()

    def updateEvolution(self):
        '''updateEvolution(self)
        Update the current evolution state of the tamagotchi based on the "lifetime" property.
        '''

        for e in EVOLUTIONS:
            if self.lifetime >= e['delta'][0] and self.lifetime < e['delta'][1]:
                self.evolution = e
                break

    def setHealth(self, h):
        '''setHealth(self, h)
        Set the health of the tamagotchi based on the h parameter.
        '''

        if h >= 0:
            self.health = h
        else:
            raise ValueError("tamagotchi's health cannot be neggative")

    def isSick(self):
        '''isSick(self)
        Determine if the tamagotchi is Sick.
        Should return True if the current instance is Sick, False otherwise.
        '''

        if self.sickness > 0:
            return True
        return False

    def fallSick(self):
        '''fallSick(self)
        Randomly made the tamagotchi fall sick, based on his current evolution.
        '''

        if randrange(SICKNESS_SCALE) < self.evolution['sickness_factor']:
            self.sickness = SICKNESS_MODIFIER

    def saveState(self):
        '''saveState(self)
        Save the current tamagotchi state in the file SAVE_FILENAME.
        '''

        f=open(SAVE_FILENAME, 'w')
        f.write(self.toJSON())
        f.close()

    def updateHunger(self):
        '''
        Update the  hunger and health of the tamagotchi.
        '''
        self.hunger = (self.hunger + HUNGER_MODIFIER) % 100
        if self.hunger > 50:
            if not self.isSick():
                self.sickness = SICKNESS_MODIFIER
            self.happiness = self.happiness - HAPPINESS_MODIFIER

    def updateSickness(self):
        '''
        Update the health and sickness state of the tamagotchi if he's sick.
        '''
        if self.isSick():
            self.sickness = self.sickness + SICKNESS_MODIFIER
            self.health = self.health - (self.sickness * 0.01)

    def update(self):
        '''update(self)
        Update the tamagotchi current state. This method should be called at each tick of the game.
        Apply the following modifier:
        - update the evolution
        - sickness modifier
        - hunger modifier
        And also save the current state. 
        '''

        logging.debug('[Tamagotchi.update()] - performing update')
        self.updateEvolution()
        self.updateHunger()
        self.updateSickness()
        
        self.fallSick()
        self.lifetime += 1
        self.saveState()

    def isDead(self):
        '''isDead(self)
        Return True if the tamagotchi is dead (health < 0). False otherwise.
        '''

        if self.health <= 0:
            return True
        return False

    def __str__(self):
        '''__str__(self)
        Serialize the Tamagotchi as a string.
        Should return a String.
        '''
        return f'Tamagotchi(health={self.health}, gender={self.gender}, hunger={self.hunger}, happiness={self.happiness}, sickness={self.sickness})'

    def activity_feeding(self):
        '''activity_feeding(self)
        Feed the tamagotchi. Feeding the tamagotchi is supposed to made him happier.
        '''

        hunger = self.hunger - HUNGER_FEED
        self.hunger = hunger if hunger >= 0 else 0

        health = self.health + 2
        self.health = health if health < 100 else 100

        happiness = (self.happiness + HAPPINESS_FEED)
        self.happiness = happiness if happiness < 100 else 100

    def activity_healing(self):
        '''activity_healing(self)
        Heal the tamagotchi.
        '''

        self.sickness = 0

    def addFriend(self, friend):
        '''addFriend(self, friend)
        Add a firen to the tamagotchi friends list.
        '''

        for f in self.friends:
            if f['name'] == friend['name']:
                return

        self.friends.append(friend)

    @staticmethod
    def fromJSON(data):
        '''fromJSON(data)
        Initialize a tamagotchi using a saved state.
        Should return a new Tamagotch instance.
        '''

        data = json.loads(data)
        return Tamagotchi(
            data['name'],
            data['health'],
            data['gender'],
            data['hunger'],
            data['happiness'],
            data['sickness'],
            data['lifetime'],
            data['friends'],
            data['scores']
        )

    def toJSON(self):
        '''toJSON(self)
        Serialize a tamagotchi as a JSON string.
        Should return a JSON string representing a Tamagotchi instance.
        '''

        obj = {
            'name' : self.name,
            'health' : self.health,
            'gender' : self.gender,
            'hunger' : self.hunger,
            'happiness' : self.happiness,
            'sickness' : self.sickness,
            'lifetime' : self.lifetime,
            'friends' : self.friends,
            'scores' : self.scores
        }
        return json.dumps(obj)