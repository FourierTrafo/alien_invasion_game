import sys
import pygame
from bullet import Bullet
from random import randint
from time import sleep

from settings import Settings
from game_stats import GameStats
from ship import Ship
from alien import Alien
from star import Star
from button import Button
from scoreboard import ScoreBoard


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
        
        # Create an instance for tracking game statistics
        self.stats = GameStats(self)
        self.sb = ScoreBoard(self)

        self.ship = Ship(self) 
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()

        self._create_fleet()
        self._create_starry_sky()
        self.game_active = False
        self.game_paused = False

        # Make the Play button.
        self.play_button = Button(self, 'Play')
        self.pause_button = Button(self, 'Pause')
       
        
    def run_game(self) -> None:
        """
        Start the main loop for the game
        """
        while True:
            self._check_events()

            if self.game_active and not self.game_paused:
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)


    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play

        Args:
            mouse_pos (tupel): mouse position when clicking the screen
        """      
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        
        if button_clicked and not self.game_active:
            self._start_new_game()

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
        self.sb.show_score()

        # Draw Pause Button when paused
        if self.game_paused:
            self.pause_button.draw_button()

        # Draw the play button if the game is inactive
        if not self.game_active:
            self.play_button.draw_button()

        
        pygame.display.flip()


    def _check_keydown_events(self, event):
        """
        Respond do keypresses

        Args:
            event (pygame keydown event): keypress event 
        """        
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True

        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True

        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

        elif event.key == pygame.K_r:
            self._start_new_game()

        elif event.key == pygame.K_p:
            self._pause_game()

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
        
 
    def _check_bullet_alien_collisions(self):
        """Resond to bullet-alien collisions
        """
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, not self.settings.bullets_piercing, True)

        if collisions:
            for aliens in collisions.values(): 
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create a new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # increase level 
            self.stats.level += 1
            self.sb.prep_level()

 
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

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
                self._ship_hit()
        
        # Looking for aliens hitting the bottom of the screen
        self._check_aliens_bottom()


    def _ship_hit(self):
        """Respond to the ship beeing hit
        """
        if self.stats.ships_left > 0:
            # Decrement ships left
            self.stats.ships_left -= 1

            self._reset_level()

            # Pause
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)


    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen.
        """
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                #Tret this the same way, as if the ship is hit
                self._ship_hit()
                break                


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


    def _reset_level(self):
        """Resets the game to the initial state for a new round
        """        
        # Get rid of remaining bullets and aliens.
        self.bullets.empty()
        self.aliens.empty()

        # Create a new fleet and center the ship
        self._create_fleet()
        self.ship.center_ship()


    def _start_new_game(self):
        """Starts a new game
        """            
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_level()
        self.game_active = True
        self.game_paused = False
        self._reset_level()
        self.settings.initialize_dynamic_settings()
        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

    def _pause_game(self):
        """Pause the game on demand when game is active
        """         
        if self.game_active:
            if self.game_paused:
                self.game_paused = False
            else:     
                self.game_paused = True
                
     
if __name__ == '__main__':
    #Make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()
