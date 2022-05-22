# from tkinter.tix import Tree
from game import Game
from threading import Thread, Lock
from tkinter import *
from tkinter import messagebox
from time import sleep
from utils import Action, Actions
import json as JSON
from logging import debug, info
import re

from network import MeetServer, MeetClient
from dinogame import DinoGame

LINE_HEIGHT = 16

class Screen:
    '''
    Abstract class that represent a screen. Handle the three button and drawing on the canvas.
    '''

    def __init__(self):
        self.current = 0

    def handleNext(self):
        '''handleNext(self)
        Handle a click on the next button.
        '''
        pass
    
    def handleBack(self):
        '''handleBack(self)
        Handle a click on the back button, the basic comportement is to decrement the current selected item.
        '''
        pass
    
    def handleSelect(self):
        '''handleSelect(self)
        Handle a click on the select button.
        '''
        pass

    def update(self):
        '''update(self)
        Update the currently displayed screen. Should be call at each tick of the game. Not mandatory.
        '''
        pass

    def initDraw(self):
        '''initDraw(self)
        Initial drawing function for the screen. Use to populate the canvas with initial sprite and text.
        '''
        pass

class Meet:
    '''Meet
    Abstract class representing the Meeting menu. Handle the submenu asking for IP addresses.
    '''

    def __init__(self):
        self.ipconfig = None

    def createIpConfig(self, msg):
        '''createIpConfig(self, msg)
        Creat the IP input window and display the message "msg" to the user.
        '''

        self.sub = Tk()
        self.sub.resizable(0,0)

        i_name = Text(self.sub, height = 1, width = 10)
        i_name.grid(column=1, row=0)
        i_name.insert(END, "127.0.0.1:1337")

        l_name = Label(self.sub, text="Name")
        l_name.grid(column=0, row=0)

        b_name = Button(self.sub, text=msg, command=lambda input=i_name : self.handleSubIpInput(input))
        b_name.grid(column=0, row=1)

        self.sub.mainloop()

    def handleSubIpInput(self, input):
        '''handleSubIpInput(self, input)
        Handle when the user has finished to write the ip. Check the ip format, and port. 
        Display error message if the formats are not correct.
        '''

        text = input.get(1.0, "end-1c")
        ip, port = text.split(':')

        if re.match('^[0-9]+$', port) == None:
            messagebox.showerror(title="Error", message="port is not numeric only")
            return
        else:
            port = int(port)
        
        if re.match('^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$', ip) == None:
            messagebox.showerror(title="Error", message="invalid IP, should be in format: 127.0.0.1:1337")
            return

        
        self.ipconfig = {'ip':ip, 'port':port}
        self.sub.quit()
        self.sub.destroy()

class MultiplayerMenuScreen(Screen):
    '''
    Menu that handle if the user want to host or join a multiplayer game.
    '''

    def __init__(self, canvas, game, parent):
        '''
        Initiaize the screen parameters, and call the initdraw method.
        '''
        Screen.__init__(self)
        self.canvas = canvas
        self.game = game
        self.parent = parent

        self.initDraw()

    def initDraw(self):
        '''
        Display the two choices to the canvas and made only the currently selected visible.
        '''
        self.choices = [
            {'handler' : self.handleJoin, 'id' : self.canvas.create_text(62, 62, anchor="c", text="Join a game", state=NORMAL)},
            {'handler':  self.handleHost, 'id' : self.canvas.create_text(62, 62, anchor="c", text="Host a game", state=HIDDEN)}
        ]
        self.choice = 0

    def handleNext(self):
        '''
        Toggle the currently selected option.
        '''
        self.choice = (self.choice + 1) % len(self.choices)
        for i in range(len(self.choices)):
            if self.choice == i:
                self.canvas.itemconfigure(self.choices[i]['id'], state=NORMAL)
            else:
                self.canvas.itemconfigure(self.choices[i]['id'], state=HIDDEN)
    
    def handleBack(self):
        '''
        Return to the parent screen.
        '''
        self.canvas.delete('all')
        self.game.currentScreen = self.parent
        self.game.currentScreen.initDraw()
    
    def handleSelect(self):
        '''
        Handle the choice of the user by calling the correct handler.
        '''
        self.choices[self.choice]['handler']()
    
    def handleHost(self):
        '''
        Change the screen to the MultiplayerHostScreen, and set the parent as the parent of the current screen, so the user will not came back to this one.
        '''
        self.canvas.delete('all')
        self.game.currentScreen = MultiplayerHostScreen(self.canvas, self.game, self.parent)

    def handleJoin(self):
        '''
        Change the screen to the MultiplayerJoinScreen, and set the parent as the parent of the current screen, so the user will not came back to this one.
        '''
        self.canvas.delete('all')
        self.game.currentScreen = MultiplayerJoinScreen(self.canvas, self.game, self.parent)

class MultiplayerHostScreen(Screen, Meet):
    '''
    Screen that handle the Hosting of a multiplayer game.
    '''

    def __init__(self, canvas, game, parent):
        '''
        Ask the user on which IP and port he want to host the game, and start a MeetServer on those.
        '''
        Screen.__init__(self)
        Meet.__init__(self)
        self.canvas = canvas
        self.game = game
        self.parent = parent

        self.ready = False
        self.finish = False
        self.score = None

        self.server_config = {}
        self.ipconfig = None
        self.createIpConfig("Create")
        
        self.initDraw()

        self.server = MeetServer(self.ipconfig, self.handleMeet)
        self.server.start()

    def initDraw(self):
        '''
        Draw a message indicating that we wait for an friend to join the game.
        '''
        self.msg = self.canvas.create_text(62, 62, anchor="c", text="waiting for a friend...", state=NORMAL)

    def handleEndGame(self, score):
        '''
        Handle that is triggered when tthe dinogame is ended. The score is passed as an argument, and is directly send to the opponent. We then wait for the opponnent to send his score. And then display if the user has win or loose.
        '''
        self.score = score
        self.canvas.itemconfigure(self.msg, text="wait for friend score")

        self.client.send(JSON.dumps({'score': score}).encode())
        data = self.client.recv(2048)
        opponent = JSON.loads(data.decode())

        self.client.send(b"ACK")
        self.client.recv(3)

        if opponent['score'] < self.score:
            self.canvas.itemconfigure(self.msg, text="You win :)")
        else:
            self.canvas.itemconfigure(self.msg, text="You loose :(")
        self.canvas.create_text(62, 62+LINE_HEIGHT, anchor="c", text="%d - %d" % (self.score, opponent['score']), state=NORMAL)

        self.client.close()
        self.client = None
        self.finish = True

    def handleBack(self):
        '''
        Close the client connection if there's one, and stop the MeetServer. Then go back to the parent screen.
        '''
        if self.client:
            self.client.close()

        self.server.stop()
        self.canvas.delete('all')
        self.game.currentScreen = self.parent
        self.game.currentScreen.initDraw()

    def handleSelect(self):
        '''
        If the game is finnished, go back to the parent screen. Else, it means that the game is not started yet, and if a client has join, we start the game.
        '''
        if self.finish:
            self.handleBack()
        elif self.ready:
            self.canvas.delete('all')
            self.game.currentScreen = MultiplayerGameScreen(self.canvas, self.game, self)

    def handleMeet(self, client):
        '''
        Handle triggered when a client connect. Then change the message to indicate that the game is ready to be started.
        '''
        self.client = client
        
        self.canvas.itemconfigure(self.msg, text="Game is ready to start...")
        self.ready = True

class MultiplayerJoinScreen(Screen, Meet):
    '''
    Screen that handle when a user want to join a multiplayer game.
    '''

    def __init__(self, canvas, game, parent):
        '''
        Initialize the screen and ask user IP and port to connect to. Then start a MeetClient to those informations.
        '''
        Screen.__init__(self)
        Meet.__init__(self)
        self.canvas = canvas
        self.game = game
        self.parent = parent

        self.finish = False
        self.ready = False

        self.server_config = {}
        self.ipconfig = None
        self.createIpConfig("Connect")
        
        self.initDraw()

        self.client = MeetClient(self.ipconfig, self.handleMeet)
        self.client.start()

    def initDraw(self):
        '''
        Display a message to the user indicating that we are trying to connect to the server.
        '''
        self.msg = self.canvas.create_text(62, 62, anchor="c", text="Tying to connect...", state=NORMAL)

    def handleEndGame(self, score):
        '''
        Handle triggered when the dinogame is ended. Then wait for server score and thensend the score, and update the screen to display the win/loose message.
        '''
        self.score = score
        self.canvas.itemconfigure(self.msg, text="wait for friend score")

        data = self.server.recv(2048)
        opponent = JSON.loads(data.decode())

        self.server.send(JSON.dumps({'score': score}).encode())
        self.server.recv(3)
        self.server.send(b"ACK")
        self.finish = True

        if opponent['score'] < self.score:
            self.canvas.itemconfigure(self.msg, text="You win :)")
        else:
            self.canvas.itemconfigure(self.msg, text="You loose :(")
        self.canvas.create_text(62, 62+LINE_HEIGHT, anchor="c", text="you: %d" % (self.score), state=NORMAL)
        self.canvas.create_text(62, 62+LINE_HEIGHT, anchor="c", text="opponent: %d" % (opponent['score']), state=NORMAL)

        self.server.close()
        self.server = None
        self.finish = True

    def handleBack(self):
        '''
        Stop the connection with the server, and then go back to the parent screen.
        '''
        if self.server:
            self.server.close()

        self.canvas.delete('all')
        self.game.currentScreen = self.parent
        self.game.currentScreen.initDraw()

    def handleSelect(self):
        '''
        If the game is finished, go back to the parent screen. Else, it means that the game is not started yet, and if we are connected to the server, we start the game.
        '''
        if self.finish:
            self.handleBack()
        elif self.ready:
            self.canvas.delete('all')
            self.game.currentScreen = MultiplayerGameScreen(self.canvas, self.game, self)

    def handleMeet(self, server):
        '''
        Handle triggered when the client is connected to the server.
        '''
        self.server = server
        self.canvas.itemconfigure(self.msg, text="Game is ready to start...")
        self.ready = True

class MultiplayerGameScreen(Screen):
    '''
    Screen that manage a multiplayer game. Very similar to GameScreen in fact.
    '''

    def __init__(self, canvas, game, parent):
        '''
        Initialize the screen, pause the game, and setup the DinoGame ready to be started.
        '''
        Screen.__init__(self)
        self.canvas = canvas
        self.game = game
        self.parent = parent

        self.game.is_paused = True

        scores = self.game.tamagotchi.scores
        highscore = max(scores) if len(scores) > 0 else 0
        self.dinoGame = DinoGame(canvas, highscore)
    
    def handleBack(self):
        '''
        Stop the dinogame, unpaude the game, and return to the parent screen.
        '''
        self.dinoGame.stop()
        
        # resume the paused tamagotchi
        self.game.is_paused = False

        # return to parent
        self.canvas.delete('all')
        self.game.currentScreen = self.parent
        self.game.currentScreen.initDraw()

        # send the score to the parent screen
        self.parent.handleEndGame(self.dinoGame.score)
    
    def handleSelect(self):
        '''
        Call the jump action of the dinogame.
        '''
        self.dinoGame.jump()

class GameScreen(Screen):
    '''GameScreen(Screen)
    Class representing the dino game activity.
    '''

    def __init__(self, canvas, game, parent):
        '''__init__(self, canvas, game, parent)
        Initialize a new GameScreen Object. Initializing this class paused the tamagotchi updat thread.
        canvas : canvas use to draw the activity.
        game : current gae object, containing tamagotchi, ...
        parent : the parent that initialize this screen.
        '''

        Screen.__init__(self)
        self.canvas = canvas
        self.game = game
        self.parent = parent

        self.game.is_paused = True

        scores = self.game.tamagotchi.scores
        highscore = max(scores) if len(scores) > 0 else 0
        self.dinoGame = DinoGame(canvas, highscore)
    
    def handleBack(self):
        '''handleBack(self)
        Save the score of the user, resume the tamagotchi update thread and return to the parent Screen.
        '''
        self.game.tamagotchi.scores.append(self.dinoGame.score)
        self.dinoGame.stop()
        
        # resume the paused tamagotchi
        self.game.is_paused = False

        # return to parent
        self.canvas.delete('all')
        self.game.currentScreen = self.parent
        self.game.currentScreen.initDraw()
    
    def handleSelect(self):
        '''handleSelect(self)
        Forward the click on the select button to the DinoGame to make the player jump.
        '''
        self.dinoGame.jump()

class MeetMainScreen(Screen):
    '''MeetMainScreen(Screen)
    Screen that ask the player if it want to create or join a meeting.
    '''

    def __init__(self, canvas, game, parent):
        '''
        Initialize the screen.
        canvas : canvas use to draw the activity.
        game : current gae object, containing tamagotchi, ...
        parent : the parent that initialize this screen.
        '''
        Screen.__init__(self)
        self.canvas = canvas
        self.game = game
        self.parent = parent
        self.initDraw()
        

    def initDraw(self):
        '''initDraw(self)
        Initialize the screen, add the two options to the canvas.
        '''

        self.choices = [
            {'handler' : self.handleJoin, 'id' : self.canvas.create_text(62, 62, anchor="c", text="Join a meet", state=NORMAL)},
            {'handler':  self.handleCreate, 'id' : self.canvas.create_text(62, 62, anchor="c", text="Create a meet", state=HIDDEN)}
        ]
        self.choice = 0

    def handleNext(self):
        '''handleNext(self)
        Change the option displayed to the user.
        '''

        self.choice = (self.choice + 1) % len(self.choices)
        for i in range(len(self.choices)):
            if self.choice == i:
                self.canvas.itemconfigure(self.choices[i]['id'], state=NORMAL)
            else:
                self.canvas.itemconfigure(self.choices[i]['id'], state=HIDDEN)

    def handleSelect(self):
        '''handleSelect(self)
        Change the screen according to the user choice either Create or Join a meet.
        '''
        self.choices[self.choice]['handler']()
    
    def handleBack(self):
        '''handleBack(self)
        Get back to the parent screen.
        '''

        debug('[?] - FrienListScreen.handleBack - ')
        self.canvas.delete('all')
        self.game.currentScreen = self.parent
        self.game.currentScreen.initDraw()

    def handleJoin(self):
        '''handleJoin(self)
        Handle the Join meeting choice. Should change the game current screen to a MeetClientScreen object.
        '''
        self.canvas.delete('all')
        self.game.currentScreen = MeetClientScreen(self.canvas, self.game, self)
    
    def handleCreate(self):
        '''handleCreate(self)
        Handle the Create meeting choice. Should change the game current screen to a MeetServerScreen object.
        '''
        self.canvas.delete('all')
        self.game.currentScreen = MeetServerScreen(self.canvas, self.game, self)

class MeetServerScreen(Screen, Meet):
    '''MeetServerScreen(Screen, Meet)
    Screen that handle meeting server.
    '''
    
    def __init__(self, canvas, game, parent):
        '''__init__(self, canvas, game, parent)
        Initialize the screen, and the MeetServer object associated.
        canvas : canvas use to draw the activity.
        game : current gae object, containing tamagotchi, ...
        parent : the parent that initialize this screen.
        '''
        Screen.__init__(self)
        Meet.__init__(self)

        self.canvas = canvas
        self.game = game
        self.parent = parent
        
        self.server_config = {}
        self.ipconfig = None
        self.createIpConfig("Create")
        
        self.msg = self.canvas.create_text(62, 62, anchor="c", text="waiting for a friend...", state=NORMAL)

        self.server = MeetServer(self.ipconfig, self.handleMeet)
        self.server.start()
    
    def handleBack(self):
        '''
        Return to the parent screen.
        '''

        debug('[?] - MeetServerScreen.handleBack - ')
        self.canvas.delete('all')
        self.game.currentScreen = self.parent
        self.game.currentScreen.initDraw()
    
    def handleMeet(self, client):
        '''handleMeet(self, client)
        Method called as a callback when the MeetServer meet someone.
        client : socket connected to he other tamagotchi.
        '''
        
        client.send(self.game.tamagotchi.toJSON().encode())
        data = client.recv(1024)
        friend = JSON.loads(data.decode())
        self.game.tamagotchi.addFriend(friend)
        debug("[+] - have meet someone : %s" % friend)
        self.canvas.itemconfigure(self.msg, text="nice to meet you")
        self.canvas.create_text(62, 62+LINE_HEIGHT, anchor="c", text=friend['name'], state=NORMAL)

class MeetClientScreen(Screen, Meet):
    '''
    Screen displayed for client meeting, ask the client the ip to connect to and handle the communication.
    '''

    def __init__(self, canvas, game, parent):
        '''
        Initialize the screen and display a message indicating that we are connecting. Also start the MeetClient, and ttry to connect to the server.
        '''
        Screen.__init__(self)
        Meet.__init__(self)
        
        self.canvas = canvas
        self.game = game
        self.parent = parent
        
        self.server_config = {}
        self.ipconfig = None
        self.createIpConfig("Connect")
        
        self.msg = self.canvas.create_text(62, 62, anchor="c", text="Tying to connect...", state=NORMAL)

        self.client = MeetClient(self.ipconfig, self.handleMeet)
        self.client.start()
    
    def handleBack(self):
        '''
        Return to the parent screen.
        '''
        print('[?] - MeetServerScreen.handleBack - ')
        self.canvas.delete('all')
        self.game.currentScreen = self.parent
        self.game.currentScreen.initDraw()
    
    def handleMeet(self, client):
        '''
        Handle the incomming connection to the server. Decode the data transmitted, and send tamagotchi informations.
        '''
        data = client.recv(1024)
        client.send(self.game.tamagotchi.toJSON().encode())
        friend = JSON.loads(data.decode())
        self.game.tamagotchi.addFriend(friend)
        print("[+] - have meet someone ! : %s" % friend)

        self.canvas.itemconfigure(self.msg, text="nice to meet you")
        self.canvas.create_text(62, 62+LINE_HEIGHT, anchor="c", text=friend['name'], state=NORMAL)

class DeathScreen(Screen):
    '''
    Screen displayed when the tamagotchi is dead
    '''

    def __init__(self, canvas, game, parent):
        '''
        Initialize the screen, and place the death message in the middle of it.
        '''
        Screen.__init__(self)
        self.canvas = canvas
        self.game = game
        self.parent = parent

        self.canvas.create_text(62, 62, anchor="c", text="You're dead")

    def handleBack(self):
        '''
        Quit the game.
        '''
        self.game.quit = True
        exit()

    def handleNext(self):
        '''
        Quit the game.
        '''
        self.handleBack()
    
    def handleSelect(self):
        '''
        Quit the game.
        '''
        self.handleBack()

class FrienListScreen(Screen):
    '''
    Screen used to display the tamagotchi friend list.
    '''

    def __init__(self, canvas, game, parent):
        '''
        Initialize the screen, and call the initDraw method.
        '''
        Screen.__init__(self)
        self.canvas = canvas
        self.game = game
        self.parent = parent

        self.initDraw()

    def initDraw(self):
        '''
        Initialize 7 line to display friend informations and update them according to the tamagotchi friend list.
        '''
        self.canvas.create_text(62, 0, anchor="n", text="Friends")
        self.lines = [self.canvas.create_text(62, LINE_HEIGHT * i, anchor="n", text="", state=HIDDEN) for i in range(1, 8)]
        self.page = 0
        self.updateDisplay()
        
    def updateDisplay(self):
        '''
        Update the friends displayed according to the current page displayed.
        '''
        if len(self.game.tamagotchi.friends) == 0:
            return

        for i in range(7):
            idx = int(i + (7 * self.page))
            if idx < len(self.game.tamagotchi.friends):
                self.canvas.itemconfigure(self.lines[i], text=self.game.tamagotchi.friends[idx]['name'])
                self.canvas.itemconfigure(self.lines[i], state=NORMAL)
            else:
                self.canvas.itemconfigure(self.lines[i], state=HIDDEN)

    def handleNext(self):
        '''
        Increase the current page counter and update the friend list.
        '''
        nbMaxPages = int(len(self.game.tamagotchi.friends)/7)
        self.page = (self.page + 1) % (nbMaxPages + 1)
        self.updateDisplay()

    def handleBack(self):
        '''
        Return to the parent screen.
        '''
        self.canvas.delete('all')
        self.game.currentScreen = self.parent
        self.game.currentScreen.initDraw()

class ShowStatsScreen(Screen):
    '''
    Class that show the stats of the current Tamagotchi.
    '''

    def __init__(self, canvas, game, parent):
        '''
        Initialize the screen, load the image, and call the initial draw function.
        '''
        Screen.__init__(self)
        self.canvas = canvas
        self.game = game
        self.parent = parent

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
        '''
        Draw the statistics to the canvas.
        '''
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
    
    def handleNext(self):
        '''
        Switch the screen to the friend list Screen.
        '''
        self.canvas.delete('all')
        self.game.currentScreen = FrienListScreen(self.canvas, self.game, self.parent)

    def handleBack(self):
        '''
        Return to the parent screen.
        '''
        self.canvas.delete('all')
        self.game.currentScreen = self.parent
        self.game.currentScreen.initDraw()

class MainScreen(Screen):
    '''
    Main screen, allow accessing to the sub menu.
    '''

    def __init__(self, canvas, game):
        '''
        Initialize the screen by preloading all the image and calling the init Draw method to display all the icons and the tamagotchi.
        '''
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
            },
            {
                'title':'multijoueur', 
                'action': self.handleMultijoueur,
                'icon_enable' : self.icon_play_enable,
                'icon_disable' : self.icon_play_disable
            }
        ]

        self.initDraw()


    def initDraw(self):
        '''
        Draw all the icon to the canvas.
        '''
        # place options
        spacing = int(124/5)
        for i in range(len(self.options)):
            o = self.options[i]
            pos = (spacing * ((i%5) + 1)) - (spacing / 2)

            y = 4 if i < 5 else 120
            anch = 'n' if i < 5 else 's'

            o['itemId_enable'] = self.canvas.create_image(pos, y, anchor=anch, image=o['icon_enable'], state=HIDDEN)
            o['itemId_disable'] = self.canvas.create_image(pos, y, anchor=anch, image=o['icon_disable'], state=NORMAL)
        
        # place tamagotchi
        pos_x = int(124/2)
        pos_y = int((124-int(124/5))/2)

        for k in self.evolutions.keys():
            for s in self.evolutions[k].keys(): 
                self.evolutions[k][s]["id"] = self.canvas.create_image(pos_x, pos_y, anchor='n', image=self.evolutions[k][s]["icon"], state=HIDDEN)

        self.update()


    def handleSelect(self):
        '''handleSelect(self)
        Handle a click on the select button, the basic comportement is to start the function associated with the options array at the current indexes.
        '''

        self.options[self.current]['action']()
        debug("[?]  - Screen.handleSelect - %s" % self.options[self.current]['title'])
    
    def handleManger(self):
        '''
        Call the feeding activity of the tamagotchi.
        '''
        debug("[+] - MainScreen.handleManger - donne a manger")
        self.game.tamagotchi.activity_feeding()

    def handleSoigner(self):
        '''
        Call the healing activity of the tamagotchi.
        '''
        self.game.tamagotchi.activity_healing()
        debug("[+] - MainScreen.handleSoigner - donne du soin")

    def handleJouer(self):
        '''
        Start the game screen.
        '''
        self.canvas.delete('all')
        self.game.currentScreen = GameScreen(self.canvas, self.game, self)

    def handleMultijoueur(self):
        '''
        Start the multiplayer game screen.
        '''
        self.canvas.delete('all')
        self.game.currentScreen = MultiplayerMenuScreen(self.canvas, self.game, self)

    def handleCommuniquer(self):
        '''
        Start the meeting screen.
        '''
        self.canvas.delete('all')
        self.game.currentScreen = MeetMainScreen(self.canvas, self.game, self)

    def handleShowStats(self):
        '''
        Start the statistics screen.
        '''
        self.canvas.delete('all')
        self.game.currentScreen = ShowStatsScreen(self.canvas, self.game, self)

    def handleNext(self):
        '''handleNext(self)
        Handle a click on the next button, the basic comportement is to increment the current selected item.
        '''

        self.current = (self.current + 1) % len(self.options)
        debug("[?]  - Screen.handleNext - current = %d" % self.current)
    
    def handleBack(self):
        '''handleBack(self)
        Handle a click on the back button, the basic comportement is to decrement the current selected item.
        '''

        if self.current - 1 < 0:
            self.current = len(self.options) - 1
        else:
            self.current -= 1
        debug("[?]  - Screen.handleBack - current = %d" % self.current)

    def update(self):
        '''
        Update the screen according to the current tamagotchi state and selected icons.
        '''

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

class UiGame(Game):
    '''
    UI game class, just handle button, and update, gives screen a canvas to draw in it, and refresh it.
    ''' 

    def __init__(self, tickrate, tamagotchi):
        '''__init__(self, tickrate, tamagotchi)
        Initialize a new UiGame instance. 
        Initiate the game parameters and Ui interface.
        '''

        Game.__init__(self, tickrate, tamagotchi)

        self.tickrate = tickrate
        self.tamagotchi = tamagotchi
        self.isPaused = False

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
        '''handleNext(self)
        General handler for the next button. The only purpose of this function is to forward the click to the handler of the currently displyed screen.
        '''

        self.currentScreen.handleNext()

    def handleSelect(self):
        '''handleSelect(self)
        General handler for the select button. The only purpose of this function is to forward the click to the handler of the currently displayed screen.
        '''

        self.currentScreen.handleSelect()

    def handleBack(self):
        '''handleBack(self)
        General handler for the back button. The only purpose of this function is to forward the click to the handler of the currently displayed screen.
        '''

        self.currentScreen.handleBack()

    def update(self):
        '''update(self)
        Method called each tick to update the screen. 
        Should display the DeathScreen if the current Tamagotchi is dead, otherwise, just call the update method of the current screen.
        '''

        if self.tamagotchi.isDead() and len(self.root.winfo_children()) > 1:
            # change to death screen ...
            self.canvas.delete('all')
            self.currentScreen = DeathScreen(self.canvas, self, None)

        self.currentScreen.update()

    def _run(self, mutex):
        '''_run(self, mutex)
        Method called each tick in order to update the current game.
        '''

        while True:
            if not self.isPaused:
                if self.isEnded():
                    self.update()
                    break

                mutex.acquire()
                self.tick()
                mutex.release()
                self.update()

            sleep(1 / self.tickrate)

    def run(self):
        '''run(self)
        Initialize the inner game thread, and lock. Then start the interface.
        '''

        self.mutex = Lock()
        t_tick = Thread(target=self._run, args=[self.mutex])
        t_tick.start()

        self.play()

    def play(self):
        '''play(self)
        Start the game interface.
        '''
        
        self.root.mainloop()
        self.quit = True