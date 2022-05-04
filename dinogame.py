from tkinter import *

CHARACTER_START_X = 16
CHARACTER_START_Y = 124-4
CHARACTER_MAX_HEIGHT = 124-64
CHARACTER_MIN_HEIGHT = CHARACTER_START_Y
CHARACTER_VELOCITY = 4
CHARACTER_GRAVITY = 2

OBSTACLE_OFFSET_Y = 248
OBSTACLE_FIRST_Y = 124
OBSTACLE_VELOCITY = 3

GROUND = 124-3

SCOREBOARD_FORMAT = 'Score: %d'
HIGHSCORE_FORMAT = 'HS: %d'

UP = 'up'
DOWN = 'down'

class Character:
    def __init__(self, item, canvas):
        self.canvas = canvas
        self.tk_item = item
        self.is_jumping = False
        self.direction = UP

    def jump(self):
        x,y = self.canvas.coords(self.tk_item)

        if self.direction == UP:
            if y - CHARACTER_VELOCITY < CHARACTER_MAX_HEIGHT:
                self.direction = DOWN
            self.canvas.move(self.tk_item, 0, -CHARACTER_VELOCITY)
        else:
            self.canvas.move(self.tk_item, 0, CHARACTER_GRAVITY)
            if y > CHARACTER_MIN_HEIGHT:
                self.canvas.coords(self.tk_item, CHARACTER_START_X, CHARACTER_START_Y)
                self.is_jumping = False

class Obstacle:
    def __init__(self, item, canvas):
        self.tk_item = item
        self.canvas = canvas
    
    def move(self):
        self.canvas.move(self.tk_item, -OBSTACLE_VELOCITY, 0)
    
    def adjust(self, model):
        x, y = self.canvas.coords(model.tk_item)
        self.canvas.coords(self.tk_item, x + OBSTACLE_OFFSET_Y, y)
    
    def offScreen(self):
        x, y = self.canvas.coords(self.tk_item)
        return x < 0

class DinoGame:
    def __init__(self, canvas, highscore):
        self.canvas = canvas

        self.ticker = 0
        self.score = 0
        self.is_stopped = False

        self.character_img = PhotoImage(file='images/balle.png')
        self.obstacle_img = PhotoImage(file='images/barriere.png')

        self.scoreboard = self.canvas.create_text(1, 0, anchor='nw', text=(SCOREBOARD_FORMAT % self.score), state=NORMAL)
        self.canvas.create_text(123, 0, anchor='ne', text=(HIGHSCORE_FORMAT % highscore), state=NORMAL)

        character_item = self.canvas.create_image(CHARACTER_START_X, CHARACTER_START_Y, anchor='s', image=self.character_img, state=NORMAL)

        self.character = Character(character_item, self.canvas)
        self.obstacles = [ 
        ]

        for i in range(10):
            self.obstacles.append(Obstacle(self.canvas.create_image(OBSTACLE_FIRST_Y + (i * OBSTACLE_OFFSET_Y), GROUND, anchor='s', image=self.obstacle_img, state=NORMAL), self.canvas))

        self.tick()

    def jump(self):
        if not self.character.is_jumping:
            self.character.is_jumping = True
            self.character.direction = UP

    def stop(self):
        self.is_stopped = True

    def updateScore(self):
        if self.ticker == 30 or self.ticker == 60:
            self.score += 1
        self.canvas.itemconfig(self.scoreboard, text=(SCOREBOARD_FORMAT % self.score))

    def isColliding(self, obstacle):
        obs_x, obs_y = self.canvas.coords(obstacle.tk_item)
        char_x, char_y = self.canvas.coords(self.character.tk_item)

        char_width = self.character_img.width()
        char_height = self.character_img.height()
        
        obs_width = self.obstacle_img.width()
        obs_height = self.obstacle_img.height()

        # correct x offset to be at sw
        obs_x = obs_x - obs_width
        char_x = char_x - char_width

        if obs_x < char_x < (obs_x + obs_width) and obs_y > char_y > (obs_y-obs_height):
           return True
        
        if obs_x < (char_x + char_width) < (obs_x + obs_width) and obs_y > char_y > (obs_y-obs_height):
           return True

        return False

    def loose(self):
        self.is_stopped = True
        self.canvas.delete('all')
        self.canvas.create_text(62, 62, anchor='c', text=(SCOREBOARD_FORMAT % self.score), state=NORMAL)

    def tick(self):
        if self.is_stopped:
            return

        if self.character.is_jumping:
            self.character.jump()

        for o in self.obstacles:
            o.move()
            if self.isColliding(o):
                self.loose()
                return

            if o.offScreen():
                o.adjust(self.obstacles[-1])
        
        self.updateScore()

        self.ticker = (self.ticker + 1) % 61
        self.canvas.after(int(1000/60), self.tick) # tickrate : 60fps
