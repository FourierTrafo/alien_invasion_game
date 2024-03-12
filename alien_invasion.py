import sys
import pygame
from bullet import Bullet
from random import randint

from settings import Settings
from ship import Ship
from alien import Alien
from star import Star


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
        self.stars = pygame.sprite.Group()

        self._create_fleet()
        self._create_starry_sky()
       
        
    def run_game(self) -> None:
        """
        Start the main loop for the game
        """
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
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
        #create background
        self.screen.fill(self.settings.bg_color)
        
        #fill background with stars
        self.stars.draw(self.screen)  

        #draw shot bullets
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
        
        self._check_bullet_alien_collisions()
        

        if not self.aliens:
            # Destroy existing bullets and create a new fleet.
            self.bullets.empty()
            self._create_fleet()

    def _check_bullet_alien_collisions(self):
        """Resond to bullet-alien collisions
        """
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, not self.settings.bullets_piercing, True)

 
    def _create_fleet(self):
        """Creates the fleet of aliens
        """  
        #Create an alien and keep adding aliens until there's no room left
        #Spacing between aliens is one alien_width       
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y  = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            current_x = alien_width       
            current_y += 2 * alien_height


    def _create_alien(self, x_position, y_position):
        """create an alien and place it in the row
        """ 
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position 
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)


    def _update_aliens(self):
        """Update the positions of all aliens in the fleet
        """
        self._check_fleet_edges()
        self.aliens.update()    


    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge
        """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction
        """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1        


    def _create_starry_sky(self):
        """Creates randomly placed stars in the background
        """
        star_count = 0

        while star_count < self.settings.stars_allowed:
            
            # Set random position
            x_position = randint(0, self.screen.get_width())
            y_position = randint(0, self.screen.get_width())

            # Set scaling, width and height should be equal
            width = randint(1, self.settings.star_scale_width)
            height = width

            # Rotate by random angle
            rotation_angle  = randint(0, 45)
            
            
            self._create_star(x_position, y_position, width, height,
                              rotation_angle) 
            
            star_count += 1


    def _create_star(self, x_position, y_position, width,
                      height, rotation_angle):
        """Create a star at the given position in the backgrond

        Args:
            x_position (int): x-Position on the screen of the star
            y_position (int): y-Position on the screen of the star
            width (int): Scale the star to given width
            height (int): Scale the star to given height
            rotation_angle (int): rotate the star around its axis by given angle
        """
        new_star = Star(self)
        new_star.rect.x = x_position
        new_star.rect.y = y_position
        new_star.scale(width, height)
        new_star.rotate(rotation_angle)
        self.stars.add(new_star)

       

if __name__ == '__main__':
    #Make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()
