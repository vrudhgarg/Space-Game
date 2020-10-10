import pygame
from settings import Settings
from ship import Ship
from game_stats import GameStats
from scoreboard import  Scoreboard
from button import Button
import game_functions as gf
from pygame.sprite import Group
def run_game():
    # Initialize pygame,settings and screen object
    pygame.init() #Initialize background settings that Pygram needs to work properly
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    #Create an instance to store game statistics and create a scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings,screen,stats)
    play_button = Button(ai_settings,screen, " Play")
    #Make a Ship
    ship = Ship(ai_settings,screen)
    #Make a group to store bullets in
    bullets = Group() #Instance of the class pygame.Sprite.Group
    aliens = Group() #Make a group of aliens
    gf.create_fleet(ai_settings, screen,ship, aliens) #Create the fleet of the aliens
    #Set the background rail
    bg_color = (230,230,230)
    #Make an alien
#Start the main loop for the game
    while True:
        #Watch for keyboard and mouse events
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)
            gf.update_aliens(ai_settings,screen,stats,sb,ship, aliens,bullets) #We'll update the positions of the aliens after updating bullets
        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets, play_button)
run_game()
