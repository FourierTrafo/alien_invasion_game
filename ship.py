import pygame

class Ship:
    """A class to manage the ship 
    """    

    def __init__(self, ai_game):
        """Initalize the ship and set its starting position
        """
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.png')
         # Resize the ship image to fit the screen
        self.image = pygame.transform.scale(self.image, (40, 80))

        self.rect = self.image.get_rect()

        self.moving_right = False
        self.moving_left = False

        # Start each new ship at the bottom center of the screen 
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self) -> None:
        """
        Draw ship at its current location
        """        
        self.screen.blit(self.image, self.rect)

    def update(self) -> None:
        """
        Update the ships position based on the movement flag
        """        
        if self.moving_right:
            self.rect.x += 1
        
        if self.moving_left:
            self.rect.x -=1
            