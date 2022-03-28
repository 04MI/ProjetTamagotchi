from tkinter import *
from time import *
import random
import sys

WIDTH = 800
HEIGHT = 600


class Dino(PhotoImage):
    def __init__(self, container, images):
        self.container = container
        self.images = images
        self.index = 0
        self.wait=False
        self.jump=False#Initial no jump so jump flag is false
        self.acc=0.5#acceleration is set to 1
        self.dir='up'#jump dir is up initially
        self.counter=0#counter will have zero value
        self.leanCount=0#this variable will help to get how long will dino duck or lean
        self.lean=False#lean variable is also false

        super().__init__()
        self.x,self.y=200, HEIGHT - 100#these are the positions of dino when game start
        print(self.x,self.y)
        self.dino_frames = self.container.create_image(self.x,self.y, image=self.images[0])#creating images of dino

        self.animate_dino()#animation the dino

    def animate_dino(self):#This function will animate dino
        if self.counter%2==0 and not self.jump and not self.lean:#in normal movement of dino,, it is necessary that it is not jumping or leaning also counter variable help in getting how often it will change picture
            self.container.itemconfig(self.dino_frames, image=self.images[self.index])#index value will update and new image of dino will be displayed
            self.index += 1#index is incremented
            if self.index == len(self.images) - 3:#checking if index number is not increasing the value of images it can access like it can access upto 7-3=4 from 0 to 4 total 5 images
                self.index = 0#set index to zero
            if self.counter==100:#checking if counter has reached its limit
                self.counter=0#set it back to zero
        if self.jump and not self.lean:# and self.counter%10==0:#if it is to jump but not to lean
            self.container.itemconfig(self.dino_frames, image=self.images[self.index])#jump the dino
            self.jump_dino()#calling jumping function
        if self.lean and self.counter%2==0 and not self.jump :#if it is to lean not to jump
            self.index+=1#updating the index
            if self.index > len(self.images) - 1:#check for the images of the dino if they are last two images whcih are for ducking or leaning dino
                self.index = 5#at index 5 and 6
            self.container.itemconfig(self.dino_frames, image=self.images[self.index])#configuring the image of dino
            self.leanCount+=1#this will help how long will it lean
            if self.leanCount>10:#if it has reahced this much 
                self.leanCount=0#then set lean variable value to zero 
                self.lean=False#set the value of lean to False
                if self.wait:
                    self.jump_dino()
                    self.wait=False
                self.index=0
            if self.counter==100:#if again counter reacches 100
                self.counter=0#set it to zero
        self.counter+=1

    def jump_dino(self):####This function will let run the animation of dinosaurus jump
        if not self.lean:
            self.jump=True#Jump flag will set to tru
            if self.dir=='up':#First dino will move up 
                x,y=0,-20#its y coordinates will decrease
                y=y+self.acc*2#This will give it some acceleration
                self.y+=y#New value of y will be store
                #print(y,self.y)
                self.acc+=0.5#acceleration
                if self.y<=HEIGHT-250:#check if dino has reached to some height
                    #exit()
                    self.acc=0.5#acceleration value will be reset
                    #print(self.x,self.y)
                    self.dir='down'#the flag will be set for down direction
            elif self.dir=='down':#Now dino will move down
                x,y=0,8#initial y and it will increase as it is accelreting
                y=y+self.acc*2#accleration of y
                self.y+=y#new value of y
                #print(y,self.y)
                self.acc+=0.5#acceleration
                if self.y>=HEIGHT-100:#if dino has reached it initial position
                    #y=self.y-(HEIGHT-100)
                    self.y=HEIGHT-100#then y position will be set to ground
                    self.dir='up'#down flag is set
                    self.jump=False#jump will be set to false to end jump
                    if self.wait:
                        self.lean_dino()
                        self.wait=False
                    self.counter=0#This counter will help in achieving jump along with other motion of the dino
                    self.acc=0.5#acceleration value is also reset
                    #print('end')
            #print(self.y)
            self.container.move(self.dino_frames,x,y)#function to move the dino on canvas
        if self.lean:
            self.wait=True

    def lean_dino(self):#This function will help in ducking or leaning
        if not self.jump:
            self.lean=True#lean variable is set true
            self.index=5#index value will help in picking two different duckking or leaned dino images at index 5,6
    
            #self.container.move(self.dino_frames,x,y)
        if self.jump:
            self.wait=True


class Nature(PhotoImage):
    def __init__(self, container, image):
        self.container = container
        self.image = image

        super().__init__()
        self.create_cactus=[self.container.create_image(WIDTH / 3+100, 495, image=self.image[4]),
            self.container.create_image(WIDTH / 3, 495, image=self.image[5]),
            self.container.create_image(WIDTH / 2+280, 495, image=self.image[6]),
            self.container.create_image(WIDTH / 2+380, 495, image=self.image[7])]#random.randrange(400, 450)
        self.create_ground = self.container.create_image(WIDTH/2, HEIGHT - 50, image=self.image[0])
        self.create_clouds = [self.container.create_image(WIDTH / 2, random.randrange(150, 400), image=self.image[1]),
                              self.container.create_image(WIDTH/4, random.randrange(150, 400), image=self.image[2]),
                              self.container.create_image(WIDTH-150, random.randrange(150, 400), image=self.image[3])]


        #self.random_cloud = random.choice(self.create_clouds)
        #self.clouds=random.sample(self.create_clouds,3)
        self.animate_ground()

    def animate_ground(self):
        (x, y) = self.container.coords(self.create_ground)#taking coordinates of the ground
        self.container.move(self.create_ground, 800, 0) if x <= 0 else self.container.move(self.create_ground, -5, 0)#moving ground to new location
        random.shuffle(self.create_clouds)
        #random.shuffle(self.create_cactus)
        random.shuffle(self.create_cactus)
        for cloud in self.create_clouds:#self.clouds:#animating clouds
            (x, y) = self.container.coords(cloud)#taking coords of each cloud
            if x <= 0:#if it is leser than 0
                self.container.move(cloud, 850, 0)#if cloud has reahced left most shift it to right most so that it can come in screen again
            else:#otherwise
                self.container.move(cloud, -3, 0)#move cloud slowly
        for cactus in self.create_cactus:#self.clouds:#animating clouds
            (x, y) = self.container.coords(cactus)#taking coords of each cloud
            
            if x <= 0:#if it is leser than 0
                self.container.move(cactus, 850, 0)#if cloud has reahced left most shift it to right most so that it can come in screen again
            else:#otherwise
                self.container.move(cactus, -3, 0)#move cloud slowly


class Obstacle(PhotoImage):
    def __init__(self, container, image):
        self.container = container
        self.image = image
        self.ind=False#indexing flag
        self.bird=False#flag to create bird
        super().__init__()
        self.ObsSets=[]
        self.ObsCombination=['1','2','4','11','11','11','11','21','21','21','12','12','12','22','22','22','3','4','4']#1 small cactus, 2 large cactus,3 rock, 4 bird
        self.combDict={'1':(54,101),'2':(37,70),'3':(49,50),'11':(54*2,101,54),'12':(54+37,101,(54+37)/2),'21':(54+37,101,(54+37)/2),'22':(37*2,70,37),'4':(68,50)}#This dictionary contains data size of different images
        #self.animate_obstacles()
    def create(self,obs,offset):
        ind=0
        for typ in obs:
            if not self.ind:
                self.obsMov=WIDTH-100#to place new obstacles
                self.ind=True
            if typ=='1':
                #creating image of big cactus
                self.ObsSets.append( ['1',self.container.create_image(WIDTH-100+ind*offset, HEIGHT-100, image=self.image[1])])
            if typ=='2':
                #creating image of small cactus
                self.ObsSets.append(['2',self.container.create_image(WIDTH-100+ind*offset, HEIGHT-90, image=self.image[0])])
            if typ=='3':
                #creating rocks
                self.ObsSets.append(['3',self.container.create_image(WIDTH-100+ind*offset, HEIGHT-70, image=self.image[2])])
            if typ=='4':
                #creating bird at different heights
                self.birdView=3#bird has image at index 3
                self.bird=True#setting this value will help in animating the bird
                self.count=0#count will let to change bird image after sometime
                self.ObsSets.append(['4',self.container.create_image(WIDTH-50+ind*offset, random.choice([HEIGHT-160,HEIGHT-120]), image=self.image[self.birdView])])#Generating two random birds at differnt positions
            ind+=1

    def animate_obstacles(self,obs):#Animating differnt obstacles
        if obs[0]=='4' and self.bird:#if obstacle is bird
            self.count+=1#increment count
            if self.count%5==0:#if count is multiple of 5
                self.birdView+=1#change index to get next image of flying bird
                if self.birdView>len(self.image)-1:#if index is out of number of images
                    self.birdView=3#reset it back to 3
                if self.count==50:#if count reaches 50
                    self.count=0#reset it too
                self.container.itemconfig(obs[1],image=self.image[self.birdView])#changing image of bird
        (x, y) = self.container.coords(obs[1])#getting coordinates of obstacle
        self.container.delete(self.ObsSets.pop(0)[1]) if x <= 0 else self.container.move(obs[1], -15, 0)#deleting obstacle if it reaches the end
        try:#just to handle error
            if self.ObsSets.index(obs)==len(self.ObsSets)-1 and x<300:#if obstacle is last one
                self.ObstacleCreateHelp()#make new obstacle
        except:
            pass
        return#this will not let the code to go to next lines
        
        if x<=0:#if x value is lesser than or equal to 0
            if self.bird and obs[0]=='4':#if obstacle is a bird
                self.bird=False
            self.newOb=True
        #print(self.container.coords(self.ObsSets[0][1])[0]-self.container.coords(self.ObsSets[-1][1])[0]>=300)
        if len(self.ObsSets)<1 or (x<400 and not len(self.ObsSets)>2 and not self.bird ):#checking if obstacles sets lits is less than 1 or x for obstacle is less than 160 and obstacles are not 2 and also not bird
            self.ObstacleCreateHelp()#This function will randomly generate obstacles

    def ObstacleCreateHelp(self):#This function help in creating obstacles
        obj=random.choice(self.ObsCombination)#it will select random obstacles from the obstacle list
        offset=0#offset for pair obstacles
        if len(obj)>=2:#if it is paired obstacle like 2 cactus
            offset=self.combDict[obj][2]#get offset
        self.create(obj,offset)#create obstacle


class DinoGame(Tk):
    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 600
        self.timS=0
        #self=root
        #different colors of the sky
        self.skyColor=['slate gray','sky blue','DeepSkyBlue2','khaki','sandy brown','orange','SteelBlue4','midnight blue','DeepSkyBlue4' , 'DeepSkyBlue4','DeepSkyBlue3']#"blue","cyan", "yellow", "magenta"]#

        super().__init__()
        self.title('Dino')



        self.width=WIDTH#700
        self.height=HEIGHT#600
        self.fileRead()
        #self.Start()


    def Start(self):
        #self.clearAll()
        #self.Background()
        self.geometry(f'{self.WIDTH}x{self.HEIGHT}')
        self.index = 0#The index value will help in changing image sof dino
        self.counter=0#this will help to animate different objects at diferent speed
        self.spd=50#speed of obstacles and ground
        self.spdD=50#speed of dino
        self.animating=True#animation variable
        self.score=0#scor of the player
        self.n=0#this will change images for ducking
        self.collide=False#this will check for collisoin
        self.restart=False#this will help in restart
        self.canvas = Canvas(self, width=self.WIDTH, height=self.HEIGHT, bg=self.skyColor[self.n])
        self.canvas.pack()

        # load the images
        self.nature_images = [PhotoImage(file='project_tests/image_obj/ground.png'),
                                    PhotoImage(file='project_tests/image_obj/cloud.png'),
                                    PhotoImage(file='project_tests/image_obj/cloud_big.png'),
                                    PhotoImage(file='project_tests/image_obj/cloud_big_full.png'),
                                    PhotoImage(file='project_tests/image_obj/cactus.png'),
                                    PhotoImage(file='project_tests/image_obj/cactus1.png'),
                                    PhotoImage(file='project_tests/image_obj/cactus2.png'),
                                    PhotoImage(file='project_tests/image_obj/cacti.png')]

        self.dino_images = [PhotoImage(file=f'project_tests/image_obj/dino{i}.png') for i in range(7)]

        self.obstacles_images = [PhotoImage(file='project_tests/image_obj/cactus-small.png'),
                                        PhotoImage(file='project_tests/image_obj/cactus-big.png'),
                                        PhotoImage(file='project_tests/image_obj/small_pixel_rock.png'),
                                        PhotoImage(file='project_tests/image_obj/Bird1.png'),
                                        PhotoImage(file='project_tests/image_obj/Bird2.png'),
                                        ]


        # pass the images in appropriate class
        self.ground = Nature(self.canvas, self.nature_images)
        self.dino = Dino(self.canvas, self.dino_images)
        self.obstacles = Obstacle(self.canvas, self.obstacles_images)
        self.Scor=self.canvas.create_text(740, 580, text=f'{self.score}'.zfill(6), fill="black", font=('Helvetica 15 bold'))#Displaying score of the game
        self.canvas.create_text(100, 20, text='High Score:'+f'{self.HighScore}'.zfill(6), fill="white", font=('Helvetica 15 bold'))#Displaying High score on the screeen
        self.canvas.create_text(350, 580, text=f'Dino Run|  Q: Quit      P: Pause    R: Restart      Esc: Back to Tamagotchi', fill="black", font=('Helvetica 10 bold'))#Displaying some short keys of the game
        self.bind('<space>',lambda x:self.dino.jump_dino() if self.animating else None)#binding space to jump
        self.bind('<Up>',lambda x:self.dino.jump_dino() if self.animating else None)#binding up to jump
        self.bind('<Down>',lambda x:self.dino.lean_dino() if self.animating else None)#bind down to duck or lean
        self.bind('<p>',lambda x:self.Stop('p'))#bind p to pause
        self.bind('<r>',lambda x:self.Restart())#bind r to restart
        self.bind('<q>',lambda x:sys.exit())#bind q to exit
        self.obstacles.ObstacleCreateHelp()#generating obstacle
        self.animations()  # call the animations

    def Restart(self):#functioon will help in restarting the game
        self.animating=False#this will animation stopper state of variable
        self.restart=True#also make sure the game is restart
        self.after_cancel(self.ani)#cancel previous animation
        self.clearAll()#clear previous graphical data
        self.Start()#start game agin

    def Stop(self,key):
        self.animating=not self.animating#changing animation variable
        if key=='p':#if p is pressed game will be paused or start
            txt='Pause'#text to display for paused
        elif key==None:#if key is not p then it means function is called by game over state
            txt='Game Over'#game over message
        if not self.animating:#if animation variable is false
            self.pause=self.canvas.create_text(self.width/2, self.height/2, text=txt, fill="black", font=('Helvetica 35 bold'))#display the message on the screen
        else:#othe wise 
            self.canvas.delete(self.pause)#delete pause value from screen

    #--------------------To Clear all in previous window----------#
    def clearAll(self):#This will destroy the background of the window just to clear every widget from the previous window
        if hasattr(self,'canvas'):#If fram is an attribute of the window object
            self.canvas.destroy()#destroy canvas window
            del(self.canvas)#The fram attribute is also deleted

    def animations(self):
        if self.animating:#checking if the game is allowed to animate looking at the animating flag
            if self.counter%(self.spd)==0:#now after certain multiple of the spd speed of obstacles and ground, animate these thing
                self.ground.animate_ground()#ground animation
            if self.counter%(self.spdD)==0:#if counter is divisible by spdD of dino then animate dino 
                self.dino.animate_dino()#during animation of dino change its images too
            if self.counter%self.spd==0:#this will animate obstacles
                #ind=1
                for obs in self.obstacles.ObsSets:#checking how many obstacles are there
                    self.obstacles.animate_obstacles(obs)#animating the obstacles
                    if self.overLp(self.obstacles, obs, *self.obstacles.combDict[obs[0]]):#checking for the collision of dino with obstacles
                        self.collide=True#if collison occur update this flag
            self.counter+=1#increment counter
            if self.counter%100==0 and self.counter!=0:#looking for counter to get 100ms to update score
                self.score+=1#update score by 1
                self.canvas.itemconfig(self.Scor, text=f'{self.score}'.zfill(6))#displaying the updated score
            if self.counter%10000==0 and self.counter!=0:#if counter has passed 10000 then update the time zone and background color
                self.n+=1#incremennt the n value it is index of colors used in the game
                if self.n>len(self.skyColor)-1:#checking if color is lesser than number of colors 
                    self.n=0#reseting the color to first color
                self.canvas.config(bg=self.skyColor[self.n])#updating the background sky color
                self.spd-=3#speeding up the animation of ground and obstacles
                if self.spd<10:#if spd reaches a certain value don't further update it
                    self.spd=10#keep it fix
            if self.counter==100000:#if counter reaches a certain limit 
                self.counter=0#resetit to prevent memory usage

        if self.collide:#if collision occur than collisoin varaiable will be set
            #self.canvas.create_oval(self.dino.x-2, self.dino.y-2,self.dino.x+2, self.dino.y+2)#
            if self.score>self.HighScore:#if score is more than high score
                self.HighScore=self.score#update high score
                self.fileWrite()#write it to file too
            self.Stop(None)#stop the game 
            self.unbind('<space>')#Unbinding all the buttons so that they are not active in other place
            self.unbind('<Up>')#unbind this so that it cannot be used after game over
            self.unbind('<Down>')#unbind this so that it cannot be used after game over
            self.unbind('<p>')#unbind this so that it cannot be used after game over
            self.after_cancel(self.ani)#canceling the animation to stop game
        if not self.collide and not self.restart:#if it is neither collison and nor restart 
            self.ani=self.after(1, self.animations)#continue animation


    def overLp(self,othr,obs,w,h):#This method will check wheter the two rectangles overlap or not
        #If one rectangle is neither left or right or up down to the other rectangle then they over lap else not
        margins=15#a margin value to help user giving some margin in collisoin
        if obs[0]=='4':#if bird is obstacle
            margins=8#change margin a little
        obs=obs[1]
        try:#to prevent error
            x,y=othr.container.coords(obs)#getting coordinates of the obstacles
            dinoH=95#dino height for upright position
            dinoW=88#width of the upright dino
            if self.dino.lean:#if it is ducked
                dinoH=60#heigth will be changed
                dinoW=118#width of the bend dino
            #print(dinoH,margins)
            x1,y1,x3,y3,X1,Y1,X3,Y3=self.dino.x-dinoW/2,self.dino.y-dinoH/2,self.dino.x+dinoW/2,self.dino.y+dinoH/2,x-w/2+margins,y-h/2+margins,x+w/2-margins,y+h/2-margins#othr.x,othr.y,othr.x+othr.w,othr.y+othr.h
            if not (x1>=X3 or X1>=x3) and not (y3<=Y1 or Y3<=y1):#if none of these conditon is true then it is not collided
                return True
            return False#If any of the above condition fails then it means that ship overlaps anyside and thus prevent from going that side
        except:
            pass

    #------------------Score--------------#
    def fileRead(self):#This will open txt file to get high score data
            f=open('Scores/Score.txt','r')#open file to read it
            title=f.readline()#removing first line
            self.HighScore=int(f.readline())#second line is high score
            #print(self.HighScore)
            f.close()#closing the file
    def fileWrite(self):#This will write score to txt
        print(self.HighScore)
        f=open('Scores/Score.txt','w')#open file to write
        f.writelines('High Score\n')#writing heading
        f.writelines(str(self.HighScore))#writing high score
        f.close()#closing file
