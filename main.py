from tamagotchi import Tamagotchi
from game import Game
import loggingS
import utils as ut
from decimal import *
# logging.basicConfig(filename='tamagotchi.log', level=logging.ERROR)

def main():


    his=ut.read_history("history.txt")
    a=float(his[0])
    b=his[1]
    c=float(his[2])
    d=float(his[3])
    e=float(his[4])
    tamagotchi =  Tamagotchi(a,b,c, d,e)
    game = Game(30, tamagotchi)
    game.run()

if __name__ == '__main__':
    main()