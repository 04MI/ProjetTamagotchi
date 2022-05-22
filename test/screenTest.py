import unittest
from uiGame import DeathScreen
from uiGame import MeetMainScreen, FrienListScreen,MultiplayerMenuScreen,GameScreen,MultiplayerGameScreen

from tkinter import *
from game import Game
from tamagotchi import Tamagotchi
from dinogame import DinoGame
from copy import copy

# MOCK
class MockedCanvas():
    def __init__(self):
        self.text = []
        self.deleted = ""
        self.state = []
        self.drawInitialized = False
        self.images = []
        self.t_after = None

    def create_text(self, x, y, anchor="c", text="", state=""):
        self.text.append(text)
        self.state.append(state)

        return len(self.state) - 1

    def itemconfigure(self, id, state="", text=""):
        if not "" == state:
            self.state[id] = state

        if not "" == text:
            self.text[id] = text

    def itemconfig(self, id, state="", text=""):
        if not "" == state:
            self.state[id] = state

        if not "" == text:
            self.text[id] = text

    def coords(self, item, x=None, y=None):
        if x == None and y == None:
            return (item.x, item.y)
        else:
            item.x = x
            item.y = y
            return None

    def move(self, item, x, y):
        item.x += x
        item.y += y

    def after(self, time, cb):
        self.t_after = time

    def delete(self, what):
        self.deleted = what
    
    def initDraw(self):
        self.drawInitialized = True

    def create_image(self, x, y, anchor="", image=None, state="normal"):
        image.x = x
        image.y = y
        image.anchor  = anchor
        image.state  = anchor
        return copy(image)

class MockedScreen():
    def __init__(self):
        self.drawed = False
        self.gameEnded = False
        self.score = 0

    def initDraw(self):
        self.drawed = True
    
    def handleEndGame(self, score):
        self.gameEnded = True
        self.score = score

class MockedGame():
    def __init__(self):
        self.currentScreen = None
        self.is_paused = False
        self.tamagotchi = None

HAS_BEEN_CALLED = False
def MockedHandler():
    global HAS_BEEN_CALLED
    HAS_BEEN_CALLED = True

# TESTS 

class DeathScreenTest(unittest.TestCase):
    def initMinimalTamagotchi():
        name = "test"
        health = 100
        gender = "male"
        hunger = 0
        happiness = 100
        sickness = 0
        lifetime = 0

        return Tamagotchi(name, health, gender, hunger, happiness, sickness, lifetime)

    def test_handleBack_ShouldExit(self):
        tama = DeathScreenTest.initMinimalTamagotchi()
        game = Game(60, tama)
        canvas = MockedCanvas()
        screen = DeathScreen(canvas, game, None)

        with self.assertRaises(SystemExit):
            screen.handleBack()

    def test_handleNext_ShouldExit(self):
        tama = DeathScreenTest.initMinimalTamagotchi()
        game = Game(60, tama)
        canvas = MockedCanvas()
        screen = DeathScreen(canvas, game, None)

        with self.assertRaises(SystemExit):
            screen.handleNext()

    def test_handleSelect_ShouldExit(self):
        tama = DeathScreenTest.initMinimalTamagotchi()
        game = Game(60, tama)
        canvas = MockedCanvas()
        screen = DeathScreen(canvas, game, None)

        with self.assertRaises(SystemExit):
            screen.handleSelect()

class MeetMainScreenTest(unittest.TestCase):
    def initMinimalTamagotchi():
        name = "test"
        health = 100
        gender = "male"
        hunger = 0
        happiness = 100
        sickness = 0
        lifetime = 0

        return Tamagotchi(name, health, gender, hunger, happiness, sickness, lifetime)

    def test_init_ShouldInitScreenWithTwoMessageInCanvas(self):
        tama = MeetMainScreenTest.initMinimalTamagotchi()
        game = Game(60, tama)
        canvas = MockedCanvas()
        
        screen = MeetMainScreen(canvas, game, None)

        self.assertEqual(2, len(canvas.text))
        self.assertTrue("Join a meet" in canvas.text)
        self.assertTrue("Create a meet" in canvas.text)

    def test_handleBack_ShouldDestroyAndReturnToParentScreen(self):
        tama = MeetMainScreenTest.initMinimalTamagotchi()
        game = Game(60, tama)
        canvas = MockedCanvas()
        parent = MockedCanvas()
        
        screen = MeetMainScreen(canvas, game, parent)
        screen.handleBack()

        self.assertTrue(parent.drawInitialized)
        self.assertEqual("all", canvas.deleted)
        self.assertEqual(parent, game.currentScreen)

    def test_handleNext_ShouldChangeTheCurrentlySelectedChoiceAndMadeItNormal(self):
        tama = MeetMainScreenTest.initMinimalTamagotchi()
        game = Game(60, tama)
        canvas = MockedCanvas()
        parent = MockedCanvas()
        
        screen = MeetMainScreen(canvas, game, parent)
        
        choice =  screen.choice
        self.assertEqual("normal", canvas.state[screen.choices[choice]['id']])

        screen.handleNext()

        self.assertEqual("normal", canvas.state[screen.choices[screen.choice]['id']])
        self.assertEqual("hidden", canvas.state[screen.choices[choice]['id']])

    def test_handleJoin_ShouldDeleteTheCurrentCanvasAndSetTheCurrentToMeetClientScreen(self):
        tama = MeetMainScreenTest.initMinimalTamagotchi()
        game = Game(60, tama)
        canvas = MockedCanvas()
        parent = MockedCanvas()
        
        screen = MeetMainScreen(canvas, game, parent)
        # TODO: find a way to overload the MeetClientScreen, to evade the ip selection.

class FrienListScreenTest(unittest.TestCase):
    def initMinimalTamagotchi():
        name = "test"
        health = 100
        gender = "male"
        hunger = 0
        happiness = 100
        sickness = 0
        lifetime = 0

        return Tamagotchi(name, health, gender, hunger, happiness, sickness, lifetime)

    def test_init_ShouldInitWithEmptyFriendList(self):
        tama = DeathScreenTest.initMinimalTamagotchi()
        game = Game(60, tama)
        canvas = MockedCanvas()
        screen = FrienListScreen(canvas, game, None)

        self.assertEqual(8, len(canvas.text))
        self.assertEqual("Friends", canvas.text[0])
        for i in range(1, len(canvas.text)):
            self.assertEqual("", canvas.text[i])
    
    def test_init_ShouldInitAndDisplay7Friends(self):
        tama = DeathScreenTest.initMinimalTamagotchi()
        tama.friends = [{"name": ("friend%d" % i)} for i in range(16)]
        game = Game(60, tama)
        canvas = MockedCanvas()
        screen = FrienListScreen(canvas, game, None)

        self.assertEqual(8, len(canvas.text))
        self.assertEqual("Friends", canvas.text[0])
        for i in range(1, len(canvas.text)):
            self.assertEqual("friend%d" % (i-1), canvas.text[i])
            self.assertEqual(canvas.state[i], "normal")

    def test_handleNext_ShouldDisplayNextSeventhFriends(self):
        tama = DeathScreenTest.initMinimalTamagotchi()
        tama.friends = [{"name": ("friend%d" % i)} for i in range(16)]
        game = Game(60, tama)
        canvas = MockedCanvas()
        screen = FrienListScreen(canvas, game, None)
        screen.handleNext()

        self.assertEqual(8, len(canvas.text))
        self.assertEqual("Friends", canvas.text[0])
        for i in range(1, len(canvas.text)):
            self.assertEqual("friend%d" % (i-1+7), canvas.text[i])
            self.assertEqual(canvas.state[i], "normal")
    
    def test_handleBack_ShouldDisplayNextSeventhFriends(self):
        tama = DeathScreenTest.initMinimalTamagotchi()
        tama.friends = [{"name": ("friend%d" % i)} for i in range(16)]
        game = Game(60, tama)
        canvas = MockedCanvas()
        parent = MockedCanvas()
        screen = FrienListScreen(canvas, game, parent)
        screen.handleBack()

        self.assertTrue(parent.drawInitialized)
        self.assertEqual("all", canvas.deleted)
        self.assertEqual(parent, game.currentScreen)

class MultiplayerMenuScreenTest(unittest.TestCase):
    def initMinimalTamagotchi():
        name = "test"
        health = 100
        gender = "male"
        hunger = 0
        happiness = 100
        sickness = 0
        lifetime = 0

        return Tamagotchi(name, health, gender, hunger, happiness, sickness, lifetime)

    def test_init_ShouldInitWithTwoMenuOptions(self):
        canvas = MockedCanvas()
        game = None
        parent = None

        screen = MultiplayerMenuScreen(canvas, game, parent)

        self.assertEqual(len(screen.choices) , 2)
    
    def test_handleBack_ShouldReturnControlToParent(self):
        canvas = MockedCanvas()
        game = MockedGame()
        parent = MockedScreen()

        screen = MultiplayerMenuScreen(canvas, game, parent)
        screen.handleBack()

        self.assertEqual(game.currentScreen, parent)
        self.assertTrue(parent.drawed)

    def test_handleNext_ShouldChangeCurrentlySelectedOptions(self):
        canvas = MockedCanvas()
        game = MockedGame()
        parent = MockedScreen()
        screen = MultiplayerMenuScreen(canvas, game, parent)

        old_choice = screen.choice

        screen.handleNext()

        self.assertNotEqual(old_choice, screen.choice)
        self.assertEqual(canvas.state[screen.choices[screen.choice]["id"]], NORMAL)
        self.assertEqual(canvas.state[screen.choices[old_choice]["id"]], HIDDEN)

    def test_handleSelect_ShouldCallTheHandlerCorrespondingToTheChoice(self):
        global HAS_BEEN_CALLED

        canvas = MockedCanvas()
        game = MockedGame()
        parent = MockedScreen()
        screen = MultiplayerMenuScreen(canvas, game, parent)

        HAS_BEEN_CALLED = False
        screen.choices[0]["handler"] = MockedHandler
        screen.choices[1]["handler"] = None
        screen.choice = 0

        screen.handleSelect()

        self.assertTrue(HAS_BEEN_CALLED)

class GameScreenTest(unittest.TestCase):
    def initMinimalTamagotchi():
        name = "test"
        health = 100
        gender = "male"
        hunger = 0
        happiness = 100
        sickness = 0
        lifetime = 0

        return Tamagotchi(name, health, gender, hunger, happiness, sickness, lifetime)

    def test_init_ShouldInitAndSetupADinoGameObject(self):
        canvas = MockedCanvas()
        game = MockedGame()
        game.tamagotchi = GameScreenTest.initMinimalTamagotchi()
        parent = None

        screen = GameScreen(canvas, game, parent)

        self.assertTrue(game.is_paused)
        self.assertIsInstance(screen.dinoGame, DinoGame)

    def test_handleBack_ShouldSaveScoreUnpauseGameAndReturnToParent(self):
        canvas = MockedCanvas()
        game = MockedGame()
        game.tamagotchi = GameScreenTest.initMinimalTamagotchi()
        parent = MockedCanvas()

        screen = GameScreen(canvas, game, parent)

        screen.dinoGame.score = 1337
        game.tamagotchi.scores = []
        game.is_paused = True

        screen.handleBack()

        self.assertFalse(game.is_paused)
        self.assertEqual(1, len(game.tamagotchi.scores))
        self.assertEqual(1337, game.tamagotchi.scores[0])
        self.assertEqual(game.currentScreen, parent)

    def test_handleSelect_ShouldCallDinoGameJump(self):
        global HAS_BEEN_CALLED

        canvas = MockedCanvas()
        game = MockedGame()
        game.tamagotchi = GameScreenTest.initMinimalTamagotchi()
        parent = MockedCanvas()

        screen = GameScreen(canvas, game, parent)

        HAS_BEEN_CALLED = False
        screen.dinoGame.jump = MockedHandler

        screen.handleSelect()

        self.assertTrue(HAS_BEEN_CALLED)

class MultiplayerGameScreenTest(unittest.TestCase):
    def initMinimalTamagotchi():
        name = "test"
        health = 100
        gender = "male"
        hunger = 0
        happiness = 100
        sickness = 0
        lifetime = 0

        return Tamagotchi(name, health, gender, hunger, happiness, sickness, lifetime)

    def test_init_ShouldInitAndSetupADinoGameObject(self):
        canvas = MockedCanvas()
        game = MockedGame()
        game.tamagotchi = MultiplayerGameScreenTest.initMinimalTamagotchi()
        parent = None

        screen = MultiplayerGameScreen(canvas, game, parent)

        self.assertTrue(game.is_paused)
        self.assertIsInstance(screen.dinoGame, DinoGame)

    def test_handleSelect_ShouldCallDinoGameJump(self):
        global HAS_BEEN_CALLED

        canvas = MockedCanvas()
        game = MockedGame()
        game.tamagotchi = MultiplayerGameScreenTest.initMinimalTamagotchi()
        parent = MockedCanvas()

        screen = MultiplayerGameScreen(canvas, game, parent)

        HAS_BEEN_CALLED = False
        screen.dinoGame.jump = MockedHandler

        screen.handleSelect()

        self.assertTrue(HAS_BEEN_CALLED)

    def test_handleBack_ShouldUnpauseGameReturnToParentAndCallEndGameCallback(self):
        global HAS_BEEN_CALLED
        canvas = MockedCanvas()
        game = MockedGame()
        game.tamagotchi = GameScreenTest.initMinimalTamagotchi()
        parent = MockedScreen()

        screen = MultiplayerGameScreen(canvas, game, parent)

        screen.dinoGame.score = 1337
        game.is_paused = True

        HAS_BEEN_CALLED = False
        screen.dinoGame.stop = MockedHandler

        screen.handleBack()

        self.assertFalse(game.is_paused)
        self.assertTrue(HAS_BEEN_CALLED)
        self.assertEqual(1337, parent.score)

if __name__ == '__main__':
    unittest.main()