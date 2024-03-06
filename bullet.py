import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class tor create bullets fired from the ship

    Args:
        Sprite (_Sprite_): Parent-class sprite
    """    
    def __init__(self, ai_game):
        """Create a bullet object at the ships current position

        Args:
            ai_game (AilenInvasion): Running Ailen_invasion 
        """        
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0, 0) and then set correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        self.y = float(self.rect.y)
    
    def update(self) -> None:
        """Move the bullet up the screen 
        """ 
        # Update the bullets y position
        self.y -= self.settings.bullet_speed
        # set rect position accordingly 
        self.rect.y = self.y       

    def draw_bullet(self) -> None:
        """Draw the bullet to the screen 
        """
        pygame.draw.rect(self.screen, self.color, self.rect)        