import sys
import pygame
from bullet import Bullet

from settings import Settings
from ship import Ship
from alien import Alien


class AlienInvasion:
    """
    Overall Class to manage game assets and behaviour
    """    
    def __init__(self):
        """
        Initialise the game and create game ressources  
        """            
        pygame.init()

        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion')
        
        self.ship = Ship(self) 
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
       
        

    def run_game(self) -> None:
        """
        Start the main loop for the game
        """
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()
            self.clock.tick(60)
            
    
    def _check_events(self) -> None:
        """
        Respond to keypresses and mouse events 
        """ 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()    
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)


    def _update_screen(self) -> None:
        """
        Update images on the screen, and flip to the new screen
        """            
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets:
            bullet.draw_bullet()
        
        self.ship.blitme()
        self.aliens.draw(self.screen)

        pygame.display.flip()


    def _check_keydown_events(self, event):
        """
        Respon do keypresses

        Args:
            event (pygame keydown event): keypress event 
        """        
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True

        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True

        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

        elif event.key == pygame.K_q:
            sys.exit()
  

    def _check_keyup_events(self, event) -> None:
        """
        Respon do key releases

        Args:
            event (pygame keyup event): key release event 
        """     
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False 

    
    def _fire_bullet(self) -> None:
        """Create a new bullet and add it to the bullets group
        """ 
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet) 

    def _update_bullets(self) -> None:
        """Update position of bullets and get rid of old bullets
        """              
        self.bullets.update()

        # delete off-screen bullets
        for bullet in self.bullets.copy():
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)
       
    def _create_fleet(self):
        """Creates the fleet of aliens
        """  
        #Create an alien and keep adding aliens until there's no room left
        #Spacing between aliens is one alien_width       
        alien = Alien(self)
        alien_width = alien.rect.width

        current_x = alien_width

        while current_x < (self.settings.screen_width - 2 * alien_width):
            new_alien = Alien(self)
            new_alien.x = current_x
            new_alien.rect.x = current_x
            self.aliens.add(new_alien)
            current_x += 2 * alien_width

        # self.aliens.add(alien)

if __name__ == '__main__':
    #Make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()
