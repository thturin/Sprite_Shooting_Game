import pygame, sys, time, random
from os import walk
from sprites import *
from random import randint
from settings import *


#lists
duck_path_list = []
dead_ducks_list = []
stick_list = []
target_path_list = []
target_coords = [[85,286],[219,114],[293,266],[500,100],[475,277],[665,285],[772,111],[957,277],[1087,110],[1177,274]]
shot_path_list = []
#setup
pygame.init()
clock = pygame.time.Clock()

#game screen
screen = pygame.display.set_mode((screen_width,screen_height))
background = pygame.image.load('graphics/stall/bg_wood-modified.png')
pygame.mouse.set_visible(False)

#sprite groups
crosshair_group = pygame.sprite.Group()
target_group = pygame.sprite.Group()
shot_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()

i=0
#obstacles
grass2= Obstacle('graphics/Stall/grass2-modified.png',screen_width/2,screen_height-300,obstacle_group)
grass2.speed=150
for _,_,img_files in walk('graphics/Duck/'):
    for image in img_files:
        if 'duck' in image:
            duck_path_list.append('graphics/Duck/'+image)
            duck = Duck('graphics/Duck/'+image,i*200,screen_height/2,target_group)
            stick = Stick('graphics/Duck/stick_metal.png',i*200,duck.rect.bottom+60,obstacle_group, duck,target_group)
        i+=1

for _,_,img_files in walk('graphics/Bullseye/'):
    for image in img_files:
        target_path_list.append('graphics/Bullseye/'+image)

for index in range (len(target_coords)):
    Target(choice(target_path_list),target_coords[index][0],target_coords[index][1],target_group)

for _,_,img_files in walk('graphics/Shot/'):
    for image in img_files:
        shot_path_list.append('graphics/Shot/'+image)

grass1 = Obstacle('graphics/Stall/grass1-modified.png',screen_width/2,screen_height-200,obstacle_group)
water2 = Obstacle('graphics/Stall/water2-modified.png',screen_width/2,screen_height-100,obstacle_group)
water2.speed = 200
water1 = Obstacle('graphics/Stall/water1-modified.png',screen_width/2,screen_height,obstacle_group)

crosshair = Crosshair('graphics/HUD/crosshair_white_large.png',crosshair_group)
rifle = Rifle('graphics/Objects/rifle.png',crosshair_group)


#MAIN
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
            for target in target_group:
                if pygame.sprite.collide_rect(target,crosshair):
                    Shot(choice(shot_path_list),pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],shot_group,target)
                    #target.kill()



    pygame.display.flip()
    screen.blit(background,(0,0))

    obstacle_group.draw(screen)
    target_group.draw(screen)
    shot_group.draw(screen)
    crosshair_group.draw(screen)

    crosshair_group.update() #will update all sprites in group simultaneously
    target_group.update(dt)
    shot_group.update()
    obstacle_group.update(dt)
    clock.tick(60)