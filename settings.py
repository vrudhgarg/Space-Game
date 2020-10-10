#Storing all the settings in one place
class Settings():
    """ A class to store all the settings of Alien Invasion"""
    def __init__(self):
        """Initialize the game's static settings"""
        #Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)

        self.ship_limit = 2
        #Bullet settings

        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60,60,60
        self.bullets_allowed = 5
        #Alien settings
        self.fleet_drop_speed = 10
        #How quickly the game speeds up
        self.speedup_scale = 1.1
        #How quickly the alien point values increase_speed
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
         # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
        #Scoring
        #Initialising in dynamic settings because we want it to chnage everytime
        #the game restarts
        self.alien_points = 50

    def increase_speed(self):
        """ Increase speed settings and alien point values """
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)