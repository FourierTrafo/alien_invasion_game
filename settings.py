
class Settings:
    """A class to store all important seetings 
    """    
    def __init__(self):
        """Initalize the games settings
        """        
        self.screen_width = 1000
        self.screen_height = 600
        self.bg_color = (0, 13, 33)
        self.frame_rate = 60

        # Ship settings
        self.ship_speed = 10