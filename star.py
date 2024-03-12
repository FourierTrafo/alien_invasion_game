import pygame
from pygame.sprite import Sprite


class Star(Sprite):
    """A class representing a single star at the screen 
    """

    def __init__(self, ai_game):
        super().__init__()
        self.settings = ai_game.settings
        self.screen = ai_game.screen

        #Load the alien image and set its rect attribute
        self.image = pygame.image.load('images/star.png')
        self.image = pygame.transform.scale(self.image,
                                             (self.settings.star_scale_width,
                                               self.settings.star_scale_height))
        self.rect = self.image.get_rect()

        #Start each star near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        