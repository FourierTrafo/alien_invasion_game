
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
        self.ship_scale_width = 40
        self.ship_scale_height = 80

        # Bullet settings 
        self.bullet_speed = 2
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (250, 250, 250)
        self.bullets_allowed = 3

        #Aien settings
        self.alien_scale_width = 60
        self.alien_scale_height = 40

        #Star settings
        self.star_scale_width = 10
        self.star_scale_height = 10
        