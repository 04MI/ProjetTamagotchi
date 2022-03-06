from tamagotchi import Tamagotchi
from game import Game
from uiGame import UiGame
import logging
import utils as ut
from decimal import *

def main():
    his = ut.read_history("history.txt")
    health    = float(his['health'])
    gender    = his['gender']
    hunger    = float(his['hunger'])
    happiness = float(his['happiness'])
    sickness  = float(his['sickness'])
    lifetime  = int(his['lifetime'])
    tamagotchi =  Tamagotchi(health, gender, hunger, happiness, sickness, lifetime)
    game = UiGame(30, tamagotchi)
    game.run()

if __name__ == '__main__':
    main()