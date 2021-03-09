"""uielements.py"""
import pygame
from pygame.sprite import Sprite

# Color RGB globals
BLUE = (106, 159, 181)
WHITE = (255, 255, 255)
BLACK = (0,0,0)

class MyImage(Sprite):
    """Class to set position and draw an image"""
    def __init__(self, screen, img_path):
        """Initialize image and set position"""
        super(MyImage, self).__init__()
        self.image = pygame.image.load(img_path)
        self.rect = self.image.get_rect()
        screen_rect = screen.get_rect()
        self.rect.centerx = screen_rect.centerx
        self.rect.top = screen_rect.top

    def draw(self,screen):
        """Draw image to screen"""
        screen.blit(self.image, self.rect)

# Draw side bar submenu
class SubMenu(Sprite):
    """A sidebar to hold buttons for game screen"""

    def __init__(self, screen):
        super().__init__()

        self.screen = screen
        self.height = 300
        self.width = 200
        self.rect = pygame.Rect(screen.get_rect().right-200,(screen.get_height() -300)/2, self.width, self.height)
        self.border = pygame.Rect(self.rect.x-2, self.rect.y-2, self.width+4, self.height+4)

    def draw(self, _):
        self.screen.fill((255,255,255), self.border)
        self.screen.fill((255,0,0),self.rect)