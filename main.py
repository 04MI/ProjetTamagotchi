from tamagotchi import Tamagotchi
from uiGame import UiMenu
import utils as ut


def main():
    his = ut.read_history("history.txt")
    health = float(his['health'])
    gender = his['gender']
    hunger = float(his['hunger'])
    happiness = float(his['happiness'])
    sickness = float(his['sickness'])
    lifetime = int(his['lifetime'])
    tamagotchi = Tamagotchi(health, gender, hunger, happiness, sickness, lifetime)
    game = UiMenu(30, tamagotchi)
    game.main()


if __name__ == '__main__':
    main()

