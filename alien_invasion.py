import sys
import pygame

from settings import Settings
from ship import Ship


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

        
    def run_game(self) -> None:
        """
        Start the main loop for the game
        """
        while True:
            self._check_events()
            self.ship.update()

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
        self.ship.blitme()

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


    def _check_keyup_events(self, event):
        """
        Respon do key releases

        Args:
            event (pygame keyup event): key release event 
        """     
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False   


if __name__ == '__main__':
    #Make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()
