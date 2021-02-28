from enum import Enum, IntEnum
from random import randint, choice
import webbrowser

import pygame
import pygame.freetype
from pygame.rect import Rect
from pygame.sprite import Sprite

import button as uibtn
import sets

# Color RGB globals
BLUE = (106, 159, 181)
WHITE = (255, 255, 255)
BLACK = (0,0,0)

class Particle():
    def __init__(self, screen):
        """Snow particles for the menu"""
        self.screen_rect = screen.get_rect()
        # location = (location_x, location_y)
        # location[0] = location_x, location[1] = location_y
        self.location = (randint(0, self.screen_rect.width),0)
        # velocity = (velocity_x, velocity_y)
        # velocity[0] = velocity_x, velocity[1] = velocity_y
        self.velocity = ((randint(-2,2))/6, 1/(randint(2,3)))

    def draw(self, screen):
        """Draw the particle as well as perform changes to location and velocity for next draw"""
        pygame.draw.circle(screen, WHITE, (self.location), 1)
        self.location = (self.location[0] + self.velocity[0], self.location[1] + self.velocity[1])
        velocity_change = (0.01 * choice([i for i in range(-1,2) if i not in [0]]))
        self.velocity = (self.velocity[0] + velocity_change, self.velocity[1])

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


class GameState(Enum):
    """Enumerated list of gamestates"""

    QUIT = -1
    TITLESCREEN = 0
    GAME = 1
    SETTINGS = 2
    STATISTICS = 3

# Enumertated integer list of ButtonEvents
class ButtonEvent(IntEnum):
    """Enumerated list of user button events"""

    QUIT = pygame.USEREVENT + 0
    PLAY = pygame.USEREVENT + 1
    SETTINGS = pygame.USEREVENT + 2
    MUTE = pygame.USEREVENT + 3
    WEB = pygame.USEREVENT + 4
    TITLE = pygame.USEREVENT + 5
    
class MusicHandler():
    """A class to play and toggle music"""

    def __init__(self):

        pygame.mixer.music.load("music\\Prelude1inCmajor.flac")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

        self.bool_playing = True


    def toggle(self):
        """Toggles music off/on based on current state"""
        if self.bool_playing:
            pygame.mixer.music.pause()
            self.bool_playing = False
        else:
            pygame.mixer.music.unpause()
            self.bool_playing = True

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

    # Declare game active boolean to manage our gamestate loop
    game_active = True

    particles = []

    # Initialize and manage pygame settings
    pygame.init()
    pygame.display.set_caption("Idlorcs")

    # Initialize music handler
    bg_music = MusicHandler()

    # Declare our screen
    screen = pygame.display.set_mode((800,600))

    # Choose initial gamestate
    game_state = GameState.TITLESCREEN

    # Loop gamestates while active
    while game_active:
        if game_state == GameState.TITLESCREEN:
            game_state = title_screen(screen, particles, bg_music)
        elif game_state == GameState.GAME:
            game_state = game_screen(screen, particles, bg_music)
        elif game_state == GameState.SETTINGS:
            game_state = settings_screen(screen, particles, bg_music)
        elif game_state == GameState.STATISTICS:
            game_state = statistics_screen(screen, particles, bg_music)
        elif game_state == GameState.QUIT:
            game_active = False
    
    # Close pygame upon exiting of gamestate loop -- quit the program
    pygame.quit()

def title_screen(screen, particles, music):
    """Initialize buttons for title screen, put into button set to handle as a whole and direct towards game loop"""

    # Initialize title screen buttons and buttonset
    btn_playgame = uibtn.Button("btn_playgame",(400,400),"Play",30,BLACK,WHITE,ButtonEvent.PLAY)
    btn_settings = uibtn.Button("btn_settings",(400,450),"Settings",30,BLACK,WHITE,ButtonEvent.SETTINGS)
    btn_quitgame = uibtn.Button("btn_quitgame",(400,500),"Quit",30,BLACK,WHITE,ButtonEvent.QUIT)
    btn_github = uibtn.Button("btn_github",(screen.get_rect().right-120, screen.get_rect().bottom-15),"Created By: Kirigaine",15,BLACK,WHITE,ButtonEvent.WEB)
    btn_music = uibtn.Button("btn_music",(screen.get_rect().left+135,screen.get_rect().bottom-15),"Music By: Steven O'Brien",15,BLACK,WHITE,ButtonEvent.WEB)
    btns_titlescreen = sets.ButtonSet(btn_playgame, btn_settings, btn_quitgame, btn_github, btn_music)

    # Initialize title screen images and imageset
    img_logo = MyImage(screen, 'images\\idlorcstemplogo.png')
    itms_titlescreen = sets.ScreenSet(img_logo)

    return game_loop(screen, btns_titlescreen, itms_titlescreen, particles, music)

def game_screen(screen, particles, music):
    """Initialize buttons for game screen, put into button set to handle as a whole and direct towards game loop"""


    # Initialize game screen buttons and buttonset
    btn_return = uibtn.Button("btn_return",(50,50),"Return",30,BLACK,WHITE,ButtonEvent.TITLE)
    btn_playgame = uibtn.Button("btn_printsmth",(400,400),"Print Something",30,BLUE,WHITE,ButtonEvent.MUTE)
    btns_gamescreen = sets.ButtonSet(btn_return, btn_playgame)

    # Initialize game screen images and imageset
    itms_gamescreen = sets.ScreenSet()

    return game_loop(screen, btns_gamescreen, itms_gamescreen, particles, music)

def settings_screen(screen, particles, music):
    """Initialize buttons for setting screen, put into button set to handle as a whole and direct towards game loop"""

    # Initialize settings screen buttons and buttonset
    btn_return = uibtn.Button("btn_return",(50,50),"Return",30,BLACK,WHITE,ButtonEvent.TITLE)
    btn_lowermusic = uibtn.Button("btn_lowermusic",(400,400),"<",30,BLACK,WHITE,ButtonEvent.MUTE)
    btn_raisemusic = uibtn.Button("btn_raisemusic",(450,400),">",30,BLACK,WHITE,ButtonEvent.MUTE)
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
    """Manage events as well as draw necessary items to screen"""
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
                mouseclick_pos = pygame.mouse.get_pos()
                buttons.anyClicked(mouseclick_pos)
            elif event.type == ButtonEvent.QUIT:
                return GameState.QUIT
            elif event.type == ButtonEvent.PLAY:
                return GameState.GAME
            elif event.type == ButtonEvent.SETTINGS:
                return GameState.SETTINGS
            elif event.type == ButtonEvent.TITLE:
                return GameState.TITLESCREEN
            elif event.type == ButtonEvent.MUTE:
                music.toggle()
            elif event.type == ButtonEvent.WEB:
                if event.button_name == "btn_github":
                    webbrowser.open('https://github.com/kirigaine', new = 2)
                elif event.button_name == "btn_music":
                    webbrowser.open('https://soundcloud.com/stevenobrien', new = 2)


        screen.fill(BLACK)
        buttons.draw(screen)
        items.draw(screen)

        if len(particles) <= 500:
            particles.append(Particle(screen))
        for particle in particles:
            particle.draw(screen)
            if particle.location[0] < 0 or particle.location[0] > screen.get_rect().width or particle.location[1] > screen.get_rect().height:
                particles.remove(particle)

        for button in buttons.buttons:
            button.update(pygame.mouse.get_pos(), mouse_up)
        pygame.display.flip()

main()
