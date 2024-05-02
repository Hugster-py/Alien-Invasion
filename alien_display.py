import sys
import pygame
from time import sleep
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from gamestats import GameStats

class AlienInvasion:
#Overall class to manage game assets and behavior
    def __init__(self):
    #Initialize the game, and create game resources
        pygame.init()
        pygame.mixer.init()
        self.settings = Settings()
        
        #sets the screen to the size of the players screen
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.settings.bg = pygame.transform.scale(self.settings.bg,(self.settings.screen_width,self.settings.screen_height))
        
        music = pygame.mixer.music.load('msc.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)

        pygame.display.set_caption ("Chase's Amazing Alien Invasion")
        
        #create instance
        self.stats = GameStats(self)
        
        #Set the background color - colors are RGB colors: a mix of red, green, blue. Each color is range of 0 to 255
        self.bg_color = (77,0,75)
        self.ship = Ship(self)

        self.bullets = pygame.sprite.Group()

        self.game_over = False
        #add in aliens
        self.aliens = pygame.sprite.Group()
        self._create_fleet()


    def run_game(self):
        # Start the main loop for the game
        while True:
            
            # Redraw the screen each pass through the loop
            self._check_events()
            # Checks to see if the game is still active
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()  # Call _update_aliens() method here
            else:
                self.aliens.empty()
                self.bullets.empty()
                self.ship.center_ship()
                self.game_over = True
            self._update_screen()
                
    def _check_events(self):
        #respond to keypresses and mouse events
        for event in pygame.event.get():
            #did the player quit?
            if event.type == pygame.QUIT:
                sys.exit()
                #did the player press a key?
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
                #did the player stop holding down a key?
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
    
    def _check_keydown_events(self,event):
        #is the key right or left arrows?
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d: 
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True
        #else the Q key to quit:
        elif event.key == pygame.K_q:
            sys.exit()
        #else the player wants to fire a bullet
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
    
    def _check_keyup_events(self,event):
        #stop holding the keys?
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False

    def _fire_bullet(self):
        #creates new bullet and it to the bullets group
        #limited to num of bullets a player can have from settings
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        #updates position of the bullets and gets ride of old ones
        self.bullets.update()
        #get rid of bullets that have disappeared off screen:
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        self._check_bullet_alien_collisions()
    
    def _check_bullet_alien_collisions(self):
        #respond to bullet-alien collisions
        #check for bullets that have hit the aliens, gets rid of both if true
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            self.stats.aliens_killed += 1
            sound = pygame.mixer.Sound('bleh.mp3')
            pygame.mixer.Sound.play(sound)
        #checks if fleet is empty and creates new fleet if so
        if not self.aliens:
            #destroys any existing bullets
            self.bullets.empty()
            self._create_fleet()
            #adds level
            self.stats.level += 1
            self.settings.level += 1 

            #level up sound
            sound = pygame.mixer.Sound('levelup.mp3')
            pygame.mixer.Sound.play(sound)  
        

    def _update_aliens(self):
        #update pos of all aliens in fleet
        #check if fleet is near an edge then updates all aliens
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("SHIP HIT!!!")
            self._ship_hit()
        self._check_aliens_bottom()
    
    def _create_fleet(self):
        aliens = Alien(self)
        alien_width, alien_height = aliens.rect.size
        available_space_x = self.settings.screen_width - (2*alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)//2 + 2
        for row_number in range(number_rows):
            for alien_number in range (number_aliens_x):
                self._create_alien(alien_number,row_number)
   
    def _create_alien(self,alien_number,row_number):
            aliens = Alien(self)
            alien_width,alien_height = aliens.rect.size
            alien_width = aliens.rect.width
            aliens.x = alien_width + 2 * alien_width * alien_number

            aliens.rect.x = aliens.x
            aliens.rect.y = alien_height + 2 * aliens.rect.height * row_number
            self.aliens.add(aliens)
    
    def _check_fleet_edges(self):
        #respond if any aliens have reached edge
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        #drop the entire fleet and change direction
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed 
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        #respond to the ship being hit by an alien

        #oof sound
        sound = pygame.mixer.Sound('ouch.mp3')
        pygame.mixer.Sound.play(sound)

        if self.stats.ships_left>0:
            #decrement the num of ships
            self.stats.ships_left -= 1

            #get rid of remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #create new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #pause for 0.5 a second
            sleep (0.5)
        else:
            self.stats.game_active = False
    
    def _check_aliens_bottom(self):
        #check if any aliens have reached the bottom of the screen
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #treat the same as ship got hit
                self._ship_hit()
                break

    def _update_screen(self):
        #update images on the screen and flip to new screen
        #redraw the images on the screen with each pass through loop
        self.screen.blit(self.settings.bg, (0,0))
        self.ship.blitme()
        #draw bullets on screen
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        

        #add in the alien killed count
        font = pygame.font.SysFont(None,40)
        alien_count_str = f"Bugs Killed: {self.stats.aliens_killed}"
        alien_killed_font = font.render(alien_count_str, True,(255,255,255))
        text_rect1 = alien_killed_font.get_rect()
        text_rect1.bottomright = self.screen.get_rect().bottomright
        self.screen.blit(alien_killed_font,text_rect1)

        #add in the level count
        font = pygame.font.SysFont(None,40)
        level_str = f'Level: {self.stats.level}'
        level_font = font.render(level_str, True,(255,255,255))
        level_rect1 = level_font.get_rect()
        level_rect1.midbottom = self.screen.get_rect().midbottom
        self.screen.blit(level_font,level_rect1)

        #add in the ships remaining count
        ships_remaining_font = font.render(f'Pets Remaining: {self.stats.ships_left}', True, (255,255,255))
        ships_rect = ships_remaining_font.get_rect()
        ships_rect.bottomleft = self.screen.get_rect().bottomleft
        self.screen.blit(ships_remaining_font,ships_rect)

        #draw the alien
        self.aliens.draw(self.screen)

        #game over count
        if self.game_over:
            text = font.render("GAME OVER!!!", True, (255, 255, 255))  # Red
            text_rect = text.get_rect()
            text_rect.center = self.screen.get_rect().center
            self.screen.blit(text, text_rect)
            
        #make the most recevntly drawn screen visible
        pygame.display.flip()
 

if __name__ == '__main__':
# Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()
   
   
quit()