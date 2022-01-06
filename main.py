from tamagotchi import Tamagotchi
from game import Game
import logging

# logging.basicConfig(filename='tamagotchi.log', level=logging.ERROR)

def main():
    tamagotchi =  Tamagotchi(10,'male', 20, 30, 40)
    game = Game(30, tamagotchi)
    game.run()

if __name__ == '__main__':
    main()