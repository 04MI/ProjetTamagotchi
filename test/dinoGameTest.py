import unittest
from unittest.mock import Mock
from copy import copy

from flask import g

from dinogame import *
from tamagotchi import Tamagotchi


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

class MockedItem():
    def __init__(self) -> None:
        self.x = 0
        self.y = CHARACTER_MIN_HEIGHT

class MockedCharacter():
    def __init__(self):
        self.hasJump = False
        self.is_jumping = False

    def jump(self):
        self.hasJump = True

class CharacterTest(unittest.TestCase):
    def test_init_ShouldInitCharacterNotJumping(self):
        canvas = MockedCanvas()
        item = MockedItem()
        character = Character(item, canvas)

        self.assertEqual(item, character.tk_item)
        self.assertFalse(character.is_jumping)
        self.assertEqual(canvas, character.canvas)
        self.assertEqual("up", character.direction)

    def test_jump_ShouldIncreaseYposition(self):
        canvas = MockedCanvas()
        item = MockedItem()
        character = Character(item, canvas)
        character.is_jumping = True

        old_y = item.y

        character.jump()

        self.assertTrue(item.y < old_y)
        self.assertEqual(UP, character.direction)
        self.assertTrue(character.is_jumping)
    
    def test_jump_ShouldChangeDirection(self):
        canvas = MockedCanvas()
        item = MockedItem()
        character = Character(item, canvas)
        character.is_jumping = True

        item.y = CHARACTER_MAX_HEIGHT+1

        character.jump()

        self.assertEqual(DOWN, character.direction)
        self.assertTrue(character.is_jumping)

    def test_jump_ShouldDecreaseYPosition(self):
        canvas = MockedCanvas()
        item = MockedItem()
        character = Character(item, canvas)

        item.y = CHARACTER_MAX_HEIGHT
        character.direction = DOWN
        character.is_jumping = True

        character.jump()

        self.assertTrue(item.y > CHARACTER_MAX_HEIGHT)
        self.assertEqual(DOWN, character.direction)
        self.assertTrue(character.is_jumping)

    def test_jump_ShouldResetJumpingFlagAndResetYPosition(self):
        canvas = MockedCanvas()
        item = MockedItem()
        character = Character(item, canvas)

        item.y = CHARACTER_MIN_HEIGHT+1
        character.direction = DOWN

        character.jump()

        self.assertEqual(item.y, CHARACTER_MIN_HEIGHT)
        self.assertFalse(character.is_jumping)

class ObstacleTest(unittest.TestCase):
    def test_move_ShouldMoveThePoisitionAccordingToVelocity(self):
        item = MockedItem()
        canvas = MockedCanvas()
        obstacle = Obstacle(item, canvas)

        old_x = item.x

        obstacle.move()

        self.assertEqual(-OBSTACLE_VELOCITY, item.x)
    
    def test_offscreen_ShouldReturnFalseIfCoordIsGreaterThanZero(self):
        item = MockedItem()
        canvas = MockedCanvas()
        obstacle = Obstacle(item, canvas)

        item.x = 1337

        self.assertFalse(obstacle.offScreen())

    def test_offscreen_ShouldReturnTrueIfCoordIsLessThanZero(self):
        item = MockedItem()
        canvas = MockedCanvas()
        obstacle = Obstacle(item, canvas)

        item.x = -1

        self.assertTrue(obstacle.offScreen())
    
    def test_adjust_ShouldSetTheCoordsOfItemAccordingToTheModelGiven(self):
        item = MockedItem()
        model = MockedItem()
        model.x = 0
        item.x = 0

        canvas = MockedCanvas()
        obstacle1 = Obstacle(model, canvas)
        obstacle = Obstacle(item, canvas)

        obstacle.adjust(obstacle1)

        self.assertEqual(OBSTACLE_OFFSET_Y, item.x)

class DinoGameTest(unittest.TestCase):
    def test_init_ShouldInitAGameAndSetupAfterToUpdate(self):
        canvas = MockedCanvas()
        game = DinoGame(canvas, 1337)

        self.assertIsInstance(game.character, Character)
        self.assertEqual(len(game.obstacles), 10)

        # assert That Obstacles are correctly spaced:
        for i in range(1, 10):
            offset  = game.obstacles[i].tk_item.x - game.obstacles[i-1].tk_item.x
            self.assertEqual(OBSTACLE_OFFSET_Y, offset)
        
        # assert Character Start at correct position
        self.assertEqual(game.character.tk_item.x, CHARACTER_START_X)
        self.assertEqual(game.character.tk_item.y, CHARACTER_START_Y)
    
    def test_jump_ShouldSetTheFlagInCharacterAndTheDirectionIfNotCurrentlyJumping(self):
        canvas = MockedCanvas()
        game = DinoGame(canvas, 1337)

        game.character.is_jumping = False

        game.jump()

        self.assertTrue(game.character.is_jumping)
        self.assertEqual(UP, game.character.direction)

    def test_jump_ShouldNotChangeDirectionIfCurrentlyJumping(self):
        canvas = MockedCanvas()
        game = DinoGame(canvas, 1337)

        game.character.is_jumping = True
        game.character.direction = DOWN

        game.jump()

        self.assertTrue(game.character.is_jumping)
        self.assertEqual(DOWN, game.character.direction)

    def test_stop_ShouldSetStoppingFlag(self):
        canvas = MockedCanvas()
        game = DinoGame(canvas, 1337)

        game.is_stopped = False

        game.stop()

        self.assertTrue(game.is_stopped)

    def test_updateScore_ShouldNotIncreaseTheScore(self):
        canvas = MockedCanvas()
        game = DinoGame(canvas, 1337)

        game.ticker = 35
        game.score = 0

        game.updateScore()

        self.assertEqual(game.score, 0)

    def test_updateScore_ShouldIncreaseTheScoreIfTickerIsAtThirtyAndUpdateTheScoreboard(self):
        canvas = MockedCanvas()
        game = DinoGame(canvas, 1337)

        game.ticker = 30
        game.score = 0

        old_scoreboard = game.canvas.text[game.scoreboard]

        game.updateScore()

        self.assertEqual(game.score, 1)
        self.assertNotEqual(old_scoreboard, game.canvas.text[game.scoreboard])

    def test_updateScore_ShouldIncreaseTheScoreIfTickerIsAtSixtyAndUpdateTheScoreboard(self):
        canvas = MockedCanvas()
        game = DinoGame(canvas, 1337)

        game.ticker = 60
        game.score = 0
        old_scoreboard = game.canvas.text[game.scoreboard]

        game.updateScore()

        self.assertEqual(game.score, 1)
        self.assertNotEqual(old_scoreboard, game.canvas.text[game.scoreboard])

    def test_loose_ShouldSetStoppedFlag(self):
        canvas = MockedCanvas()
        game = DinoGame(canvas, 1337)
        game.is_stopped = False

        game.loose()

        self.assertTrue(game.is_stopped)

    def test_isColliding_ShouldNotBeCollidingIfXOffsetIsGreaterThanCharacterWidth(self):
        '''
            +--++--+
            |c || O|
            +--++--+  
        '''

        canvas = MockedCanvas()
        game = DinoGame(canvas, 1337)

        game.character.tk_item.x = 0
        game.character.tk_item.y = 0
        game.character.tk_item.w = 10
        game.character.tk_item.h = 10

        obstacle = Obstacle(PhotoImage(), canvas)
        obstacle.tk_item.x = 11
        obstacle.tk_item.y = 0
        obstacle.tk_item.w = 10
        obstacle.tk_item.h = 10

        self.assertFalse(game.isColliding(obstacle))

    def test_isColliding_ShouldNotBeCollidingIfYCharacterPositionIsGraterThanObstacleHeigth(self):
        '''
            +--+
            |c |
            +--+
            +--+
            |o |
            +--+  
        '''

        canvas = MockedCanvas()
        game = DinoGame(canvas, 1337)

        game.character.tk_item.x = 0
        game.character.tk_item.y = 11
        game.character.tk_item.w = 10
        game.character.tk_item.h = 10

        obstacle = Obstacle(PhotoImage(), canvas)
        obstacle.tk_item.x = 0
        obstacle.tk_item.y = 0
        obstacle.tk_item.w = 10
        obstacle.tk_item.h = 10

        self.assertFalse(game.isColliding(obstacle))
    
    def test_isColliding_ShouldBeCollidingIfYCharacterPositionIsLessThanObstacleHeigth(self):
        '''
            +--+
            |c |
            +--+
            +o-+
            +--+  
        '''

        canvas = MockedCanvas()
        game = DinoGame(canvas, 1337)

        game.character.tk_item.x = 0
        game.character.tk_item.y = 0
        game.character.tk_item.w = 10
        game.character.tk_item.h = 10

        obstacle = Obstacle(PhotoImage(), canvas)
        obstacle.tk_item.x = 0
        obstacle.tk_item.y = 5
        obstacle.tk_item.w = 10
        obstacle.tk_item.h = 10

        self.assertTrue(game.isColliding(obstacle))
    
    def test_isColliding_ShouldBeCollidingIfXCharacterPositionIsLessThanObstacleHeigth(self):
        '''
            +-++-+
            |o|+c|
            +-++-+
        '''

        canvas = MockedCanvas()
        game = DinoGame(canvas, 1337)

        game.character.tk_item.x = 5
        game.character.tk_item.y = 0
        game.character.tk_item.w = 10
        game.character.tk_item.h = 10

        obstacle = Obstacle(PhotoImage(), canvas)
        obstacle.tk_item.x = 0
        obstacle.tk_item.y = 0
        obstacle.tk_item.w = 10
        obstacle.tk_item.h = 10

        self.assertTrue(game.isColliding(obstacle))

    def test_isColliding_ShouldBeCollidingIfXCharacterPositionIsLessThanObstacleWidthAndYPositionILessThanObstacleHeight(self):
        '''
              +--+
            +-|+c|
            |o+--+
            +--+
        '''

        canvas = MockedCanvas()
        game = DinoGame(canvas, 1337)

        game.character.tk_item.x = 5
        game.character.tk_item.y = 5
        game.character.tk_item.w = 10
        game.character.tk_item.h = 10

        obstacle = Obstacle(PhotoImage(), canvas)
        obstacle.tk_item.x = 0
        obstacle.tk_item.y = 10
        obstacle.tk_item.w = 10
        obstacle.tk_item.h = 10

        self.assertTrue(game.isColliding(obstacle))
    
    def test_isColliding_ShouldBeCollidingIfXCharacterPositionPlusWidthIsBetweenObstaclePositionAndWidthAndYPositionILessThanObstacleHeight(self):
        
        canvas = MockedCanvas()
        game = DinoGame(canvas, 1337)

        game.character.tk_item.x = 5
        game.character.tk_item.y = 5
        game.character.tk_item.w = 10
        game.character.tk_item.h = 10

        obstacle = Obstacle(PhotoImage(), canvas)
        obstacle.tk_item.x = 10
        obstacle.tk_item.y = 10
        obstacle.tk_item.w = 10
        obstacle.tk_item.h = 10

        self.assertTrue(game.isColliding(obstacle))

    def test_tick_ShouldIncreaseTickerAndSetupAfter(self):
        canvas = MockedCanvas()
        game = DinoGame(canvas, 1337)

        game.ticker = 0

        game.tick()

        self.assertEqual(1, game.ticker)
        self.assertEqual(TICK_INTERVAL, canvas.t_after)

    def test_tick_ShouldSetTickerToZero(self):
        canvas = MockedCanvas()
        game = DinoGame(canvas, 1337)

        game.ticker = 60

        game.tick()

        self.assertEqual(0, game.ticker)

    def test_tick_ShouldNotUpdateScoreIfStoppedFlagIsSet(self):
        canvas = MockedCanvas()
        game = DinoGame(canvas, 1337)

        game.is_stopped = True
        game.ticker = 30 # already tested, should increase the score if updateScore is called.

        game.score = 1337

        game.tick()

        self.assertEqual(1337, game.score)

    def test_tick_ShouldCallCharacterJumpMethodIfFlagSet(self):
        canvas = MockedCanvas()
        game = DinoGame(canvas, 1337)

        game.character = MockedCharacter()
        game.character.is_jumping = True
        game.obstacles = [] # to skip treatement on obstacles, we are not testing this here.

        game.tick()

        self.assertTrue(game.character.hasJump)

    def test_tick_ShouldNotCallCharacterJumpMethodIfFlagNotSet(self):
        canvas = MockedCanvas()
        game = DinoGame(canvas, 1337)

        game.character = MockedCharacter()
        game.character.is_jumping = False
        game.obstacles = [] # to skip treatement on obstacles, we are not testing this here.

        game.tick()

        self.assertFalse(game.character.hasJump)

    def test_tick_ShouldMoveTheObstacle(self):
        canvas = MockedCanvas()
        game = DinoGame(canvas, 1337)

        game.obstacles = [Obstacle(PhotoImage(), canvas)]
        game.obstacles[0].tk_item.x = 1337

        game.tick()

        self.assertEqual(1337-OBSTACLE_VELOCITY, game.obstacles[0].tk_item.x)
    
    def test_tick_ShouldStopTheGameIfColliding(self):
        canvas = MockedCanvas()
        game = DinoGame(canvas, 1337)

        obstacle = Obstacle(PhotoImage(), canvas)
        obstacle.tk_item.x = OBSTACLE_VELOCITY
        obstacle.tk_item.y = 0

        character = Character(PhotoImage(), canvas)
        character.tk_item.x = 0
        character.tk_item.y = 0

        game.obstacles = [obstacle]
        game.character = character

        game.tick()

        self.assertTrue(game.is_stopped)

    def test_tick_ShouldAdjustObstaclePositionIfOffscreen(self):
        canvas = MockedCanvas()
        game = DinoGame(canvas, 1337)

        obstacle1 = Obstacle(PhotoImage(), canvas)
        obstacle1.tk_item.x = -10
        obstacle1.tk_item.y = 0

        obstacle2 = Obstacle(PhotoImage(), canvas)
        obstacle2.tk_item.x = 10
        obstacle2.tk_item.y = 0


        game.obstacles = [obstacle1, obstacle2]

        game.tick()

        self.assertEqual(obstacle1.tk_item.x, obstacle2.tk_item.x+OBSTACLE_OFFSET_Y)