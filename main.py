import pygame, sys, time
from os import walk
from random import randint

class Crosshair(pygame.sprite.Sprite):
    def __init__(self, picture_path, group):
        super().__init__()
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


class Target(pygame.sprite.Sprite):
    def __init__(self,picture_path, pos_x,pos_y,group):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x,pos_y]
        self.direction = pygame.math.Vector2(1,1)
        self.speed = 200
        group.add(self)

    def update(self,dt):
        if self.direction.magnitude()!=0:
            self.direciton = self.direction.normalize()

        self.rect.centerx += self.direction.x * self.speed * dt

        if self.rect.right > screen_width:
            self.rect.centerx=0
        #self.rect.centery += self.direction.y * self.speed * dt


#setup
pygame.init()
clock = pygame.time.Clock()

#game screen
screen_width = 1280
screen_height = 820
screen = pygame.display.set_mode((screen_width,screen_height))
background = pygame.image.load('graphics/stall/bg_blue-modified.png')
pygame.mouse.set_visible(False)

#crosshair
crosshair_group = pygame.sprite.Group()
target_group = pygame.sprite.Group()
targets=[]

i=0
j=0
for _,_,img_files in walk('graphics/Objects/'):
    for image in img_files:
        if 'duck' in image:
            target = Target('graphics/Objects/'+image,i*200,100,target_group)
            i+=1
            #targets.append(target)
        if 'target' in image:
            target = Target('graphics/Objects/' + image, j*200, 300,target_group)
            j+=1

crosshair = Crosshair('graphics/HUD/crosshair_white_large.png',crosshair_group)
rifle = Rifle('graphics/Objects/rifle.png',crosshair_group)

last_time = time.time()
while True:
    #delta time
    dt = time.time() - last_time
    last_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            #what happens when you click mouse button
            pass

    pygame.display.flip()
    screen.blit(background,(0,0))
    target_group.draw(screen)

    crosshair_group.draw(screen)

    crosshair_group.update() #will update all sprites in group simultaneously
    target_group.update(dt)
    clock.tick(60)