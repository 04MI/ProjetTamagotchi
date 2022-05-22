from tamagotchi import Tamagotchi
from game import Game
from uiGame import UiGame
import logging
import utils as ut
from decimal import *
from os.path import exists

from tkinter import *

from random import choices

name = ""

def nameCallback(input, frame):
    global name
    name = input.get(1.0, "end-1c")
    frame.destroy()

def main():
    global name

    tamagotchi = None

    if exists("history.json"):
        data = open("history.json").read()
        tamagotchi = Tamagotchi.fromJSON(data)
    else:
        root = Tk()

        i_name = Text(root, height = 1, width = 10)
        i_name.grid(column=1, row=0)

        l_name = Label(root, text="Name")
        l_name.grid(column=0, row=0)

        b_name = Button(root, text="Create", command=lambda input=i_name,frame=root:nameCallback(input, frame))
        b_name.grid(column=0, row=1)

        root.mainloop()
        tamagotchi =  Tamagotchi(name,100, choices(['male', 'female']), 0, 100, 0, 0)

    game = UiGame(30, tamagotchi)
    game.run()


if __name__ == '__main__':
    main()