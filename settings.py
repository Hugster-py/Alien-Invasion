import pygame
from gamestats import GameStats

class Settings:
    #a class to store all the settings of Alien invasion

    def __init__(self):
        #initialize settings
        #screen settings
        self.screen_width = 1200
        self.screen_height = 800
        #default color to imperial purple
        self.bg = pygame.image.load("latest.jpg")
        self.bg = pygame.transform.scale(self.bg,(self.screen_width,self.screen_height))
        self.bg_color = (77,0,75)
        self.level = 1

        #ship settings
        self.ship_speed = 5
        self.ship_limit = 3


        #bullet settings - dark grey bullets that a re 3 pixels wide and 15 pixels high. Travel slower than ship
        self.bullet_speed = 1.5
        self.bullet_width = 3 *self.level
        self.bullet_height = 45
        self.bullet_color = (255,49,49)
        self.bullets_allowed = 5 + self.level


        #alien settings
        self.alien_speed = 1 + (self.level * 2.0)
        self.fleet_drop_speed = 10 + (self.level*2.0)

        #fleet direction 1 represents right, -1 = left
        self.fleet_direction = 1

