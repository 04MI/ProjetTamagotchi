from game import Game
from threading import Thread, Lock
from tkinter import *
from time import sleep
from utils import Action, Actions
from logging import debug, info

'''
Super class that represent a typical screen, every screen should herit from this one in order to handle next, back, select button and update.
'''
class Screen:
    def __init__(self):
        self.current = 0

    def handleNext(self):
        print(len(self.options))
        self.current = (self.current + 1) % len(self.options)
        debug("[?]  - Screen.handleNext - current = %d" % self.current)
    
    def handleBack(self):
        if self.current - 1 < 0:
            self.current = len(self.options) - 1
        else:
            self.current -= 1
        debug("[?]  - Screen.handleBack - current = %d" % self.current)
    
    def handleSelect(self):
        self.options[self.current]['action']()
        debug("[?]  - Screen.handleSelect - %s" % self.options[self.current]['title'])

    def update(self):
        pass

'''
screen displayed when the tamagotchi is dead
'''
class DeathScreen(Screen):
    def __init__(self, canvas, game, parent):
        Screen.__init__(self)
        self.canvas = canvas
        self.game = game
        self.parent = parent

        self.canvas.create_text(62, 62, anchor="c", text="You're dead")

    def initDraw(self):
        pass

    def handleBack(self):
        self.game.quit = True
        exit()

    def handleNext(self):
        self.game.quit = True
        exit()
    
    def handleSelect(self):
        self.game.quit = True
        exit()

'''
screen used to display the tamagotchi friend list
'''
class FrienListScreen(Screen):
    def __init__(self, canvas, game, parent):
        Screen.__init__(self)
        self.canvas = canvas
        self.game = game
        self.parent = parent

        self.canvas.create_text(62, 62, anchor="c", text="Friends")

    def initDraw(self):
        pass

    def handleNext(self):
        pass

    def handleSelect(self):
        pass
    
    def handleBack(self):
        debug('[?] - FrienListScreen.handleBack - ')
        self.canvas.delete('all')
        self.game.currentScreen = self.parent
        self.game.currentScreen.initDraw()

'''
show the stats of the current tamagotchi
'''
class ShowStatsScreen(Screen):
    def __init__(self, canvas, game, parent):
        Screen.__init__(self)
        self.canvas = canvas
        self.game = game
        self.parent = parent

        self.icon          = PhotoImage(file = "images/perso_resize.png")

        # TODO : use real image not placeholder ...
        self.i_male        = PhotoImage(file = "images/menu_disabled_placeholder.png")
        self.i_female      = PhotoImage(file = "images/menu_enabled_placeholder.png")

        self.food_empty    = PhotoImage(file="images/pomme_disable.png")
        self.food_filled   = PhotoImage(file="images/pomme_enable.png")

        self.health_empty  = PhotoImage(file="images/coeur_disable.png")
        self.health_filled = PhotoImage(file="images/coeur_enable.png")


        # place food
        self.foods = []
        self.healths = []

        self.initDraw()

    def initDraw(self):
        spacing = int(124/5)

        # gender
        if self.game.tamagotchi.gender == "male":
            self.canvas.create_image(0, 0, anchor='w', image=self.i_male, state=NORMAL)
        else:
            self.canvas.create_image(0, 0, anchor='w', image=self.i_female, state=NORMAL)

        # the name of the tamagotchi
        y_pos = (spacing * 1)
        x_pos = (spacing * 1) - (spacing / 2)
        self.canvas.create_text(y_pos, x_pos, anchor="w", text=self.game.tamagotchi.name)
        
        # food indicator
        for i in range(1, 6):
            y_pos = (spacing * i) - (spacing / 2)
            x_pos = (spacing * 3) - (spacing / 2)

            enable = self.canvas.create_image(y_pos, x_pos, anchor='c', image=self.food_filled, state=NORMAL)
            disable = self.canvas.create_image(y_pos, x_pos, anchor='c', image=self.food_empty, state=HIDDEN)
            
            self.foods.append([enable, disable])
        
        y = 0
        for i in range(0,100,20):
            if i <= (100-int(self.game.tamagotchi.hunger)):
                self.canvas.itemconfigure(self.foods[y][0], state=NORMAL)
                self.canvas.itemconfigure(self.foods[y][1], state=HIDDEN)
            else:
                self.canvas.itemconfigure(self.foods[y][1], state=NORMAL)
                self.canvas.itemconfigure(self.foods[y][0], state=HIDDEN)
            y += 1
        
        # health indicator
        for i in range(1, 6):
            y_pos = (spacing * i) - (spacing / 2)
            x_pos = (spacing * 2) - (spacing / 2)

            enable = self.canvas.create_image(y_pos, x_pos, anchor='c', image=self.health_filled, state=NORMAL)
            disable = self.canvas.create_image(y_pos, x_pos, anchor='c', image=self.health_empty, state=HIDDEN)
            
            self.healths.append([enable, disable])
        
        y = 0
        for i in range(0,100,20):
            if i <= int(self.game.tamagotchi.health):
                self.canvas.itemconfigure(self.healths[y][0], state=NORMAL)
                self.canvas.itemconfigure(self.healths[y][1], state=HIDDEN)
            else:
                self.canvas.itemconfigure(self.healths[y][0], state=HIDDEN)
                self.canvas.itemconfigure(self.healths[y][1], state=NORMAL)
            y += 1

    def handleSelect(self):
        debug('[?] - ShowStatsScreen.handleSelect - ')
        pass
    
    def handleNext(self):
        debug('[?] - ShowStatsScreen.handleNext - ')
        self.canvas.delete('all')
        self.game.currentScreen = FrienListScreen(self.canvas, self.game, self)

    def handleBack(self):
        debug('[?] - ShowStatsScreen.handleBack - ')
        self.canvas.delete('all')
        self.game.currentScreen = self.parent
        self.game.currentScreen.initDraw()

    def update(self):
        pass

'''
main screen, allow accessing to the sub menu
'''
class MainScreen(Screen):
    def __init__(self, canvas, game):
        Screen.__init__(self)
        self.canvas = canvas
        self.game = game

        # placeholder
        self.icon_disable = PhotoImage(file = "images/menu_disabled_placeholder.png")
        self.icon_enable = PhotoImage(file = "images/menu_enabled_placeholder.png")

        # info
        self.icon_info_disable = PhotoImage(file = "images/info_disable.png")
        self.icon_info_enable  = PhotoImage(file = "images/info_enable.png")

        # manger
        self.icon_eat_disable = PhotoImage(file = "images/pomme_disable.png")
        self.icon_eat_enable  = PhotoImage(file = "images/pomme_enable.png")

        # soigner
        self.icon_heal_disable = PhotoImage(file = "images/soin_disable.png")
        self.icon_heal_enable  = PhotoImage(file = "images/soin_enable.png")

        # jouer
        self.icon_play_disable = PhotoImage(file = "images/manette_disable.png")
        self.icon_play_enable  = PhotoImage(file = "images/manette_enable.png")

        # communiquer
        self.icon_comm_disable = PhotoImage(file = "images/connection_disable.png")
        self.icon_comm_enable  = PhotoImage(file = "images/connection_enable.png")

        # tamagotchi state
        self.evolutions = {
            "BABY"  : {
                "NORMAL" : { "icon" : PhotoImage(file = "images/petit_souriant.png"), "id" : None },
                "SICK"   : { "icon" : PhotoImage(file = "images/petit_malade.png"),   "id" : None },
                "HUNGRY" : { "icon" : PhotoImage(file = "images/petit_faim.png"),     "id" : None } 
            },
            "CHILD"  : {
                "NORMAL" : { "icon" : PhotoImage(file = "images/enfant_souriant.png"), "id" : None },
                "SICK"   : { "icon" : PhotoImage(file = "images/enfant_malade.png"),   "id" : None },
                "HUNGRY" : { "icon" : PhotoImage(file = "images/enfant_faim.png"),     "id" : None } 
            },
            "ADULT" : {
                "NORMAL" : { "icon" : PhotoImage(file = "images/adulte_souriant.png"), "id" : None },
                "SICK"   : { "icon" : PhotoImage(file = "images/adulte_malade.png"),   "id" : None },
                "HUNGRY" : { "icon" : PhotoImage(file = "images/adulte_faim.png"),     "id" : None } 
            },
            "ELDER" : {
                "NORMAL" : { "icon" : PhotoImage(file = "images/adulte_souriant.png"), "id" : None },
                "SICK"   : { "icon" : PhotoImage(file = "images/adulte_malade.png"),   "id" : None },
                "HUNGRY" : { "icon" : PhotoImage(file = "images/adulte_faim.png"),     "id" : None } 
            },
        }

        self.options = [
            {
                'title':'infos', 
                'action': self.handleShowStats,
                'icon_enable' : self.icon_info_enable,
                'icon_disable' : self.icon_info_disable
            },
            {
                'title':'manger', 
                'action': self.handleManger, 
                'icon_enable' : self.icon_eat_enable,
                'icon_disable' : self.icon_eat_disable
            },
            {
                'title':'soigner', 
                'action': self.handleSoigner,
                'icon_enable' : self.icon_heal_enable,
                'icon_disable' : self.icon_heal_disable
            },
            {
                'title':'jouer', 
                'action': self.handleJouer,
                'icon_enable' : self.icon_play_enable,
                'icon_disable' : self.icon_play_disable
            },
            {
                'title':'commmuniquer', 
                'action': self.handleCommuniquer,
                'icon_enable' : self.icon_comm_enable,
                'icon_disable' : self.icon_comm_disable
            }
        ]

        self.initDraw()


    def initDraw(self):
        # place options
        i = 1
        for o in self.options:
            spacing = int(124/5)
            pos = (spacing * i) - (spacing / 2)
            o['itemId_enable'] = self.canvas.create_image(pos, 4, anchor='n', image=o['icon_enable'], state=HIDDEN)
            o['itemId_disable'] = self.canvas.create_image(pos, 4, anchor='n', image=o['icon_disable'], state=NORMAL)
            i += 1
        
        # place tamagotchi
        pos_x = int(124/2)
        pos_y = int((124-int(124/5))/2)

        for k in self.evolutions.keys():
            for s in self.evolutions[k].keys(): 
                self.evolutions[k][s]["id"] = self.canvas.create_image(pos_x, pos_y, anchor='n', image=self.evolutions[k][s]["icon"], state=HIDDEN)

        self.update()


    def handleSelect(self):
        debug('[?] - MainScreen.handleSelect - %s' % self.options[self.current]["title"])
        Screen.handleSelect(self)
    
    def handleManger(self):
        debug("[+] - MainScreen.handleManger - donne a manger")
        self.game.tamagotchi.activity_feeding()

    def handleSoigner(self):
        self.game.tamagotchi.activity_healing()
        debug("[+] - MainScreen.handleSoigner - donne du soin")

    def handleJouer(self):
        debug("[+] - MainScreen.handleJouer - Not implemented yet")
        pass

    def handleCommuniquer(self):
        debug("[+] - MainScreen.handleCommuniquer - Not implemented yet")
        pass

    def handleShowStats(self):
        self.canvas.delete('all')
        self.game.currentScreen = ShowStatsScreen(self.canvas, self.game, self)
        debug("[+] - MainScreen.handleSoigner - go to ShowStatsScreen")

    def update(self):
        debug("[?] - MainScreen.update - update")

        # update currently selectionned icon
        for i in range(len(self.options)):
            itemId_enable = self.options[i]["itemId_enable"]
            itemId_disable = self.options[i]["itemId_disable"]

            if i == self.current:
                self.canvas.itemconfigure(itemId_enable, state=NORMAL)
                self.canvas.itemconfigure(itemId_disable, state=HIDDEN)
            else:
                self.canvas.itemconfigure(itemId_disable, state=NORMAL)
                self.canvas.itemconfigure(itemId_enable, state=HIDDEN)

        # update the current tamagotchi according to his state
        # TODO : may use constant later
        state = "SICK" if self.game.tamagotchi.isSick() else "HUNGRY" if self.game.tamagotchi.hunger >= 80 else "NORMAL"
        for k in self.evolutions.keys():
            for s in self.evolutions[k].keys():
                if self.game.tamagotchi.evolution['state'] == k and s == state:
                    self.canvas.itemconfigure(self.evolutions[k][s]["id"], state=NORMAL)
                else:
                    self.canvas.itemconfigure(self.evolutions[k][s]["id"], state=HIDDEN)

'''
UI game class, just handle button, and update, gives screen a canvas to draw in it, and refresh it.
'''
class UiGame(Game):
    def __init__(self, tickrate, tamagotchi):
        Game.__init__(self, tickrate, tamagotchi)

        self.tickrate = tickrate
        self.tamagotchi = tamagotchi

        self.root = Tk()
        self.root.resizable(0,0)

        self.canvas = Canvas(self.root, width=124, height=124)
        self.canvas.config(background='#FFFFFF')
        self.canvas.grid(row=0, column=0, columnspan=3)
        
        self.currentScreen = MainScreen(self.canvas, self)

        self.b_next =  Button(self.root, text="next", command=self.handleNext)
        self.b_next.grid(row=1, column=0)

        self.b_select = Button(self.root, text="select", command=self.handleSelect)
        self.b_select.grid(row=1, column=1)

        self.b_previous = Button(self.root, text="back", command=self.handleBack)
        self.b_previous.grid(row=1, column=2)

    def handleNext(self):
        self.currentScreen.handleNext()

    def handleSelect(self):
        self.currentScreen.handleSelect()

    def handleBack(self):
        self.currentScreen.handleBack()

    def update(self):
        if self.tamagotchi.isDead() and len(self.root.winfo_children()) > 1:
            # change to death screen ...
            self.canvas.delete('all')
            self.currentScreen = DeathScreen(self.canvas, self, None)
        self.currentScreen.update()

    def _run(self, mutex):
        while True:
            if self.isEnded():
                self.update()
                break

            mutex.acquire()
            self.tick()
            mutex.release()
            self.update()
            sleep(1 / self.tickrate)

    def run(self):
        self.mutex = Lock()
        t_tick = Thread(target=self._run, args=[self.mutex])
        t_tick.start()

        self.play()

    def play(self):
        self.root.mainloop()
        self.quit = True