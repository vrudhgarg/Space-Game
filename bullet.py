import pygame
from pygame.sprite import Sprite    #Sprite helps to group elements in the game and act on all the elements at once

class Bullet(Sprite):
    """ A class to manage bullets fired from ship """
    def __init__(self, ai_settings, screen, ship):
        """ Create a Bullet object at the ship's current position"""
        super().__init__() #To inherit properties from sprite
        self.screen = screen
        #Create a bullet rect at (0,0) and then set the correct position
        self.rect = pygame.Rect(0,0,ai_settings.bullet_width,ai_settings.bullet_height) #Creating bullet at top left corner
        self.rect.centerx = ship.rect.centerx #Ship center is equal to bullet center
        self.rect.top = ship.rect.top #bullet top is equal to ship top so that it can looks like that bullet is emerging from ship's top
        #Store's the ship postion as a decimal value
        self.y = float(self.rect.y) #Can make fine adjustments to ship speed

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """ Move the bullet up the screen """
        #Update the decimal position of the bullet
        self.y -= self.speed_factor
        #Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """ Draw the bullet to the screen """
        pygame.draw.rect(self.screen, self.color,self.rect)
