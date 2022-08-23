import pygame
from settings import *
from random import *

class Generic(pygame.sprite.Sprite):
    def __init__(self,picture_path,group):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        group.add(self)

class Crosshair(Generic):
    def __init__(self, picture_path, group):
        super().__init__(picture_path,group)
        #self.image = pygame.Surface([width,height]) #emtpy surface
        #self.image.fill(color)
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect() #takes the image and draws an rectangle around it
        #self.rect.center = (pos_x,pos_y)
        group.add(self)
    def update(self): #update() is predefined in the original sprite class
        self.rect.center = pygame.mouse.get_pos() #cross hair follows mouse

class Rifle(Crosshair):
    def update(self):
        pos = [pygame.mouse.get_pos()[0]+80,pygame.mouse.get_pos()[1]+180]
        self.rect.center = pos

class Target(Generic):
    def __init__(self,picture_path, pos_x,pos_y,group):
        super().__init__(picture_path,group)
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x,pos_y]
        self.direction = pygame.math.Vector2(1,1)
        self.speed = 200
        group.add(self)

class Duck(Target):
    def __init__(self, picture_path,pos_x, pos_y, group):
        super().__init__(picture_path,pos_x,pos_y,group)

    def update(self,dt):
        if self.direction.magnitude()!=0:
            self.direction = self.direction.normalize()

        self.rect.centerx += self.direction.x * self.speed * dt

        if self.rect.right > screen_width+500:
            self.rect.centerx= -200

class Stick(Target):
    def __init__(self,picture_path, pos_x,pos_y,group, duck, target_group):
        super().__init__(picture_path,pos_x,pos_y,group)
        self.duck = duck
        self.target_group = target_group
    def check_duck_killed(self): #this function checks to see if the duck was killed (removed from target group)
        if len(self.duck.groups())==0: # this means the duck sprite is not apart of any group
           self.target_group.add(self.duck) #add the duck back to target gruoup

    def update(self,dt):
        if self.direction.magnitude()!=0:
            self.direction = self.direction.normalize()

        self.rect.centerx += self.direction.x * self.speed * dt

        if self.rect.right > screen_width+500:
            self.rect.centerx= -200
            self.duck.rect.centerx=self.rect.centerx #you need this in order to update the position of the stick when the duck is repositioned to the left hand side of the screen
            self.check_duck_killed() #add duck back to stick if the stick is to the left of the screen

class Obstacle(Target):
    def __init__(self,picture_path, pos_x,pos_y,group):
        super().__init__(picture_path, pos_x,pos_y,group)
        self.speed = 100
    def update(self,dt):
        step=100
        if self.direction.magnitude()!=0:
            self.direction = self.direction.normalize()

        self.rect.centerx += self.direction.x * self.speed * dt
        #print('left coord: {} and right coord: {} and x direction: {}'.format(self.rect.left,self.rect.right, self.direction.x))
        if self.rect.right >screen_width+step:
            self.rect.right = screen_width+step #this line is very important
            self.direction.x *=-1
        elif self.rect.left<-step:
            self.rect.left =-step
            self.direction.x *=-1

class Shot(Target):
    def __init__(self,picture_path,pos_x,pos_y,group, target):
        super().__init__(picture_path,pos_x,pos_y,group)
        self.target = target

        def update(self):
            print('hello hello')
            self.direction = self.target.direction
            self.rect.center = self.target.rect.center