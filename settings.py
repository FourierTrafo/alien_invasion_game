
class Settings:
    """A class to store all important seetings 
    """    
    def __init__(self):
        """Initalize the games settings
        """
        # Screen settings        
        self.screen_width = 1000
        self.screen_height = 600
        self.bg_color = (0, 13, 33)
        self.frame_rate = 60

        # Static Ship settings
        self.ship_scale_width = 40
        self.ship_scale_height = 80
        self.ship_limit = 2

        # Static Bullet settings 
        self.bullet_width = 300
        self.bullet_height = 15
        
        #Alien settings
        self.alien_scale_width = 60
        self.alien_scale_height = 40
        self.alien_speed = 5
        self.fleet_drop_speed = 1

        #Star settings
        self.star_scale_width = 10
        self.star_scale_height = 10
        self.star_rotation = 0
        self.stars_allowed = 50

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game
        """ 
        # Dynamic Ship settings
        self.ship_speed = 10

        # Dynamic Bullet settings
        self.bullet_speed = 5
        self.bullets_piercing = False
        self.bullet_color = (250, 250, 250)
        self.bullets_allowed = 3

        # Dynamic alien settings
        self.alien_speed = 5
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings
        """        
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
