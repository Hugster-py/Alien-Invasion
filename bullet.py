import pygame
import random
#when you use sprites, your can group related elements in your game and act on all the grouped elements at once

from pygame.sprite import Sprite

class Bullet(Sprite):
    #a class to manage bullets from the ship


    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        #randomizes bullet color
        bullet_colors = [(255,255,255), (255,0,0), (255,0,255),(254,125,25),(214,237,240)]
        self.color = (random.choice(bullet_colors))

        #create a bullet rect at (0,0) and then set correct position
        self.rect = pygame.Rect(0,0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        #store the bullets positon as a decimal value
        self.y = float(self.rect.y)

    def update(self):
        #move the bullet up the screen
        #update the decimal point of the bullet
        self.y -= self.settings.bullet_speed

        #update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        #draw the bullet to the screen
        pygame.draw.rect(self.screen, self.color,self.rect)