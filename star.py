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

        #Scale the star to default size
        self.scale(self.settings.star_scale_width, 
                   self.settings.star_scale_height)
     
        #Rotate the star by the default angle
        self.rotate(self.settings.star_rotation)
        
        self.rect = self.image.get_rect()

        #Start each star near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

    def rotate(self, rotation_angle):
      """Rotate the star image by the given angle

      Args:
          rotation_angle (int): Rotation angle
      """        
      self.angle = rotation_angle
      self.image = pygame.transform.rotate(self.image, self.angle)

    def scale(self, width, height):
      """Scale the star

      Args:
          width (int): Width the star is scaled to
          height (int): Height the star is scaled to
      """       
      self.image = pygame.transform.scale(self.image, (width, height))
                                           

        

        