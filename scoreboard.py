import pygame.font
from pygame.sprite import Group
from ship import Ship
class Scoreboard():
    """ A class to report scoring information """
    def __init__(self,ai_settings,screen,stats):
        """Initialize scoring attributes"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        #Font settings for scoring information
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None,48)
        #Score image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """ Turn the score into a rendered image """
        #Passing a negative integer to the round function as a second paramter rounds the
        #function to multiples of 10,100,1000 and so on
        rounded_score = round(self.stats.score, -1)
        #Line below adds commas to the numbers and input it as strings
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str,True,self.text_color,self.ai_settings.bg_color)
        #Display the score at top right corner
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """ Turns the high score into a rendered image """
        high_score = round(self.stats.high_score,-1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str,True,self.text_color,self.ai_settings.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """ Turns the level into a rendered image """
        self.level_image = self.font.render(str(self.stats.level),True,self.text_color,self.ai_settings.bg_color)
        #Position the level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self): #Creates an empty group, self.ships, to hold the ship instances
        """ Show how many ships are left"""
        self.ships = Group() #To fill this group a loop runs once for every ship the player has left
        for ship_number in range(self.stats.ships_left + 1):
            #Inside the loop we create a new ship and set each ship’s x-coordinate value
            #so the ships appear next to each other with a 10-pixel margin on the
            # left side of the group of ships
            ship = Ship(self.ai_settings,self.screen)
            ship.rect.x = 10 + ship_number*ship.rect.width
            # y-coordinate value 10 pixels down from the top of the
            # screen so the ships line up with the score image
            ship.rect.y = 10
            self.ships.add(ship) #adds new ship to the each group

    def show_score(self):
        """Draw scores and ships to the screen"""
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image,self.level_rect)
        self.ships.draw(self.screen)
