import pygame
import random

class Ship:
    #class to manage ship
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        #loads the choices for the ship images not scaled
        images = ["file (1).bmp", "ship2.bmp"]
        #picks a random image for the ship to be
        images1 = [pygame.image.load(f) for f in images]
        random_image = random.choice(images1)
        #have to resize my image because it is way too big.
        self.image = pygame.transform.scale(random_image, (150, 150))
        self.rect = self.image.get_rect()

        #start each new ship at bottom of center of screen
        self.rect.midbottom = self.screen_rect.midbottom

        #store a decimal value for horizontal position
        self.x = float(self.rect.x)

        #movement flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        #update the ships positon based on move flags
        #update ships x value, not rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left>0:
            self.x -= self.settings.ship_speed
        
        #update the rect object from self x
        self.rect.x = self.x

    def blitme(self):
        #draw ship in current location
        self.screen.blit(self.image,self.rect)
    
    def center_ship(self):
        #center the ship on the screen
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)