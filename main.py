from tamagotchi import Tamagotchi
from game import Game
import logging
from random import choice, random, randrange


# logging.basicConfig(filename='tamagotchi.log', level=logging.ERROR)

health_Max = 50
hunger_Max = 50
happiness_Max = 50
sickness_Max = 50
gender_type = ['"male"','"female"']

def main():
    tamagotchi =  Tamagotchi(randrange(40,health_Max),choice(['male','female']),randrange(40,hunger_Max),randrange(40,happiness_Max),randrange(40,sickness_Max))
    game = Game(30, tamagotchi)
    game.run()

if __name__ == '__main__':
    main()