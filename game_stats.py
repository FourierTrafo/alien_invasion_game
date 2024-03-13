import json
import os

class GameStats:
    """Track statistics for alien invasion
    """ 

    def __init__(self, ai_game):
        """Initialize statistics

        Args:
            ai_game (AlienInvasion): Running Instance of Alien_invasion
        """
        self.settings = ai_game.settings
        self.reset_stats()
        self.prep_high_score()
        


    def reset_stats(self):
        """Initalize statistics that can change during the game.
        """
        self.ships_left = self.settings.ship_limit
        self.score = 0                    
        self.level = 1
    
    def prep_high_score(self):
        """Loads the high score from previous games
        """ 
        high_score_save = 'high_score.json'

        if os.path.exists(high_score_save):
            with open(high_score_save, "r") as json_datei:
                data = json.load(json_datei)
            
            self.high_score = data
        else:
            self.high_score = 0