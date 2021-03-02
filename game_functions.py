import pygame
import settings
import myparticles
import webbrowser
from enum import Enum, IntEnum
BLACK = (0,0,0)

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
    MENU_BUTTON = pygame.USEREVENT + 0

def update_screen(screen, buttons, items, particles):
    screen.fill(BLACK)
    buttons.draw(screen)
    items.draw(screen)

    mouse_up = False
    if particles is not None:
        if len(particles) <= 500:
            particles.append(myparticles.SnowParticle(screen))
        for particle in particles:
            particle.draw(screen)
            if particle.location[0] < 0 or particle.location[0] > screen.get_rect().width or particle.location[1] > screen.get_rect().height:
                particles.remove(particle)

    for button in buttons.buttons:
        button.update(pygame.mouse.get_pos(), mouse_up)

    pygame.display.flip()

def check_events(buttons, music):
    #mouse_up = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return GameState.QUIT
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            check_mouse_events(buttons)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                return GameState.QUIT
        elif event.type == ButtonEvent.MENU_BUTTON:
            return check_menu_events(event, music)

def check_mouse_events(buttons):
    #mouse_up = True
    mouseclick_pos = pygame.mouse.get_pos()
    buttons.anyClicked(mouseclick_pos)

def check_menu_events(event, music):
    if event.type == ButtonEvent.MENU_BUTTON:
        if event.button_name == "btn_playgame":
            return GameState.GAME
        elif event.button_name == "btn_settings":
            return GameState.SETTINGS
        elif event.button_name == "btn_quitgame":
            return GameState.QUIT
        elif event.button_name == "btn_github":
            webbrowser.open('https://github.com/kirigaine', new = 2)
        elif event.button_name == "btn_music":
            webbrowser.open('https://soundcloud.com/stevenobrien', new = 2)
        elif event.button_name == "btn_return":
            return GameState.TITLESCREEN
        elif event.button_name == "btn_printsmth" or "btn_lowermusic" or "btn_raisemusic":
            music.toggle()