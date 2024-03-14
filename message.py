import pygame.font

class Message:
    """A class for printing long messages on the screen
    """    

    def __init__(self, ai_game, long_msg):
        """Initialize message

        Args:
            ai_game (AlienInvasion): Running AlienInvasion game
            long_msg (str): long message with \n
        """        

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the bottons
        self.width, self.height = 200, 50
        self.button_color = self.settings.bg_color
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build the messages rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The button message needs to be prepped only once
        self._prep_msg(long_msg)

    def _prep_msg(self, long_msg):
        """Turn long message into a rendered image on the screen center

        Args:
            long_msg (str): Long message containing \n
        """        

        lines = long_msg.split('\n')
        self.rendered_lines = []
        for line in lines:
            rendered_line = self.font.render(line, True, self.text_color, 
                                             self.button_color)
            self.rendered_lines.append(rendered_line)

        self.rendered_rects = [rendered_line.get_rect() for rendered_line 
                          in self.rendered_lines]
        
    def draw_msg(self):
        """Draws the Message to the screen
        """        

        total_height = sum(rect.height for rect in self.rendered_rects)
        start_y = self.rect.centery - total_height // 2

        for i, (rendered_line, rendered_rect) in enumerate(
                              zip(self.rendered_lines, self.rendered_rects)):
            rendered_rect.midtop = (self.rect.centerx,
                  start_y + sum(rect.height for rect in self.rendered_rects[:i]))
            self.screen.blit(rendered_line, rendered_rect)