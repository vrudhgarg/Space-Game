import pygame.font
class Button():
    def __init__(self,ai_settings,screen,msg):
        """Initialize button attributes """
        self.screen = screen
        self.screen_rect = screen.get_rect()

        #Set the dimensions and properties of the button
        self.width,self.height = 200,50
        self.button_color = (0,255,0)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None,48) #The None argument tells Pygame to use the default font, and 48 determines the size of the text

        #Build the button's rect object and center it
        self.rect = pygame.Rect(0,0,self.width,self.height) #To center the button on the screen
        self.rect.center = self.screen_rect.center
#Pygame works with text by rendering the string you want to display as an image.
        self.prep_msg(msg)

    def prep_msg(self,msg):
        """Turn msg into a rendered image and center text on the button."""
        #Turns the text into a image # boolean value for making edges smoother or not
        self.msg_image = self.font.render(msg,True,self.text_color,self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        #Draw blank button and then draw message
        self.screen.fill(self.button_color, self.rect) #To draw the rectangular portion of the button
        self.screen.blit(self.msg_image,self.msg_image_rect)    #Text image to the screen
