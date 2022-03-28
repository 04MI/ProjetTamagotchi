from tamagotchi import Tamagotchi
from game import Game
from uiGame import UiGame
import logging
import utils as ut
from decimal import *


def main():
    his = ut.read_history("history.txt")
    health    = round(float(his['health']),3)
    gender    = his['gender']
    hunger    = round(float(his['hunger']),3)
    happiness = round(float(his['happiness']),3)
    sickness  = round(float(his['sickness']),3)
    lifetime  = int(his['lifetime'])
    tamagotchi =  Tamagotchi(health, gender, hunger, happiness, sickness, lifetime)
    game = UiGame(30, tamagotchi)
    game.run()

if __name__ == '__main__':
    main()