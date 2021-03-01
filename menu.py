#from random import randint, choice
import webbrowser

import pygame
import pygame.freetype
#from pygame.rect import Rect
from pygame.sprite import Sprite

import button as uibtn
import game_functions as gf
import sets, settings, myparticles

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

    def draw_menu(self):
        self.screen.fill((255,255,255), self.border)
        self.screen.fill((255,0,0),self.rect)

def main():
    """Main logic loop of application"""

    game_settings = settings.Settings()

    # Declare game active boolean to manage our gamestate loop
    game_active = True

    particles = []

    # Initialize and manage pygame settings
    pygame.init()
    pygame.display.set_caption("Idlorcs")

    # Initialize music handler
    bg_music = settings.MusicHandler(game_settings)

    # Declare our screen
    screen = pygame.display.set_mode((800,600))

    # Choose initial gamestate
    game_state = gf.GameState.TITLESCREEN

    # Loop gamestates while active
    while game_active:
        if game_state == gf.GameState.TITLESCREEN:
            game_state = title_screen(screen, particles, bg_music)
        elif game_state == gf.GameState.GAME:
            game_state = game_screen(screen, particles, bg_music)
        elif game_state == gf.GameState.SETTINGS:
            game_state = settings_screen(screen, particles, bg_music)
        elif game_state == gf.GameState.STATISTICS:
            game_state = statistics_screen(screen, particles, bg_music)
        elif game_state == gf.GameState.QUIT:
            game_active = False
    
    # Close pygame upon exiting of gamestate loop -- quit the program
    pygame.quit()

def title_screen(screen, particles, music):
    """Initialize buttons for title screen, put into button set to handle as a whole and direct towards game loop"""

    # Initialize title screen buttons and buttonset
    btn_playgame = uibtn.Button("btn_playgame",(400,400),"Play",30,BLACK,WHITE,gf.ButtonEvent.MENU_BUTTON)
    btn_settings = uibtn.Button("btn_settings",(400,450),"Settings",30,BLACK,WHITE,gf.ButtonEvent.MENU_BUTTON)
    btn_quitgame = uibtn.Button("btn_quitgame",(400,500),"Quit",30,BLACK,WHITE,gf.ButtonEvent.MENU_BUTTON)
    btn_github = uibtn.Button("btn_github",(screen.get_rect().right-120, screen.get_rect().bottom-15),"Created By: Kirigaine",15,BLACK,WHITE,gf.ButtonEvent.MENU_BUTTON)
    btn_music = uibtn.Button("btn_music",(screen.get_rect().left+135, screen.get_rect().bottom-15),"Music By: Steven O'Brien",15,BLACK,WHITE,gf.ButtonEvent.MENU_BUTTON)
    btns_titlescreen = sets.ButtonSet(btn_playgame, btn_settings, btn_quitgame, btn_github, btn_music)

    # Initialize title screen images and imageset
    img_logo = MyImage(screen, 'images\\idlorcstemplogo.png')
    itms_titlescreen = sets.ScreenSet(img_logo)

    return game_loop(screen, btns_titlescreen, itms_titlescreen, particles, music)

def game_screen(screen, particles, music):
    """Initialize buttons for game screen, put into button set to handle as a whole and direct towards game loop"""

    # Initialize game screen buttons and buttonset
    btn_return = uibtn.Button("btn_return",(50,50),"Return",30,BLACK,WHITE,gf.ButtonEvent.MENU_BUTTON,screen.get_rect().top)
    btn_printsmth = uibtn.Button("btn_printsmth",(400,400),"Print Something",30,BLACK,WHITE,gf.ButtonEvent.MENU_BUTTON)
    btns_gamescreen = sets.ButtonSet(btn_return, btn_printsmth)

    # Initialize game screen images and imageset
    itms_gamescreen = sets.ScreenSet()

    return game_loop(screen, btns_gamescreen, itms_gamescreen, particles, music)

def settings_screen(screen, particles, music):
    """Initialize buttons for setting screen, put into button set to handle as a whole and direct towards game loop"""

    # Initialize settings screen buttons and buttonset
    btn_return = uibtn.Button("btn_return",(50,50),"Return",30,BLACK,WHITE,gf.ButtonEvent.MENU_BUTTON,screen.get_rect().top)
    btn_lowermusic = uibtn.Button("btn_lowermusic",(400,400),"<",30,BLACK,WHITE,gf.ButtonEvent.MENU_BUTTON)
    btn_raisemusic = uibtn.Button("btn_raisemusic",(450,400),">",30,BLACK,WHITE,gf.ButtonEvent.MENU_BUTTON)
    # music_slider = settings.PercentBar("Music",0.1,True,btn_lowermusic,btn_raisemusic,(200,0),screen.get_rect().top)
    btns_settingsscreen = sets.ButtonSet(btn_return, btn_lowermusic, btn_raisemusic)
    # Initialize settings screen images and imageset
    itms_settingsscreen = sets.ScreenSet()

    return game_loop(screen, btns_settingsscreen, itms_settingsscreen, particles, music)


def statistics_screen(screen, particles, music):
    """Initialize buttons for statistics screen, put into button set to handle as a whole and direct towards game loop"""


    # Initialize statistics screen buttons and buttonset
    btns_statisticsscreen = sets.ButtonSet()

    # Initialize statistics screen images and imageset
    itms_statisticsscreen = sets.ScreenSet()

    return game_loop(screen, btns_statisticsscreen, itms_statisticsscreen, particles, music)

def game_loop(screen, buttons, items, particles, music):
    """Manage events as well as update screen"""
    while True:
        gs_change = gf.check_events(buttons, music)
        if isinstance(gs_change, gf.GameState):
            return gs_change

        gf.update_screen(screen, buttons, items, particles)

main()
