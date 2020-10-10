class GameStats():
    """ Track statistics for alien Invasion"""
    def __init__(self,ai_settings):
        #Initialize statistics
        self.ai_settings = ai_settings
        self.reset_stats()
        #Start alien Invasion in active state
        self.game_active = True
        #Start game in inactive state
        self.game_active = False
        #High score should never be reset that's why we are defining it in init method
        self.high_score = 0

    def reset_stats(self):
        """ Initialize statistics that can change during the game"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
