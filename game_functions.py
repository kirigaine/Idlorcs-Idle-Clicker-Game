"""game_functions.py"""
import webbrowser
from enum import Enum, IntEnum
import pygame
import particles

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

def update_screen(screen, buttons, items, g_settings, zparticles, percentbars):
    """Update screen for every frame. Fill the screen, draw given objects, indicate button hovers, handle snow particles, and flip the display"""
    screen.fill(BLACK)
    buttons.draw(screen)
    items.draw(screen)
    if percentbars is not None:
        percentbars.draw(screen,g_settings)

    # If particles is an open array (like on the menu) append, iterate, and draw the particles
    if zparticles is not None:
        if len(zparticles) <= g_settings.screen_resolution[0]:
            zparticles.append(particles.SnowParticle(screen))
        for particle in zparticles:
            particle.draw(screen)
            if particle.location[0] < 0 or particle.location[0] > screen.get_rect().width or particle.location[1] > screen.get_rect().height:
                zparticles.remove(particle)

    # Provide mouse_position and mouse_up to buttons to trigger hover state
    mouse_up = False
    for button in buttons.buttons:
        button.update(pygame.mouse.get_pos(), mouse_up, g_settings)

    pygame.display.flip()

def check_events(buttons, music, sound, g_settings):
    """Check generic or highest abstraction events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return GameState.QUIT
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            check_mouse_events(buttons)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                return GameState.QUIT
        elif event.type == ButtonEvent.MENU_BUTTON:
            return check_menu_events(event, music, sound, g_settings)

def check_mouse_events(buttons):
    """Get the mouse position as well as check buttons set of menu buttons for click position"""
    mouseclick_pos = pygame.mouse.get_pos()
    buttons.anyClicked(mouseclick_pos)

def check_menu_events(event, music, sound, g_settings):
    """Check the menu buttons click events"""
    if event.type == ButtonEvent.MENU_BUTTON:
        # TITLE SCREEN
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
        # SETTINGS SCREEN
        elif event.button_name == "btn_return" or event.button_name == "btn_titlescreen":
            return GameState.TITLESCREEN
        elif event.button_name == "btn_fullscreentoggle":
            g_settings.fullscreen = not g_settings.fullscreen
            if g_settings.fullscreen:
                g_settings.screen_resolution = g_settings.monitor_size
                pygame.display.set_mode(g_settings.monitor_size,pygame.FULLSCREEN)
            else:
                g_settings.screen_resolution = (g_settings.screen_width, g_settings.screen_height)
                pygame.display.set_mode(g_settings.screen_resolution)
            return GameState.SETTINGS
        elif event.button_name == "btn_musictoggle":
            g_settings.music_on = not g_settings.music_on
            music.toggle(g_settings)
        elif event.button_name == "btn_soundtoggle":
            g_settings.sound_on = not g_settings.sound_on
        elif event.button_name == "btn_lowermusic":
            music.lower_volume(g_settings)
        elif event.button_name == "btn_raisemusic":
            music.raise_volume(g_settings)
        elif event.button_name == "btn_lowersound":
            sound.lower_volume(g_settings)
        elif event.button_name == "btn_raisesound":
            sound.raise_volume(g_settings)
        
        # GAME SCREEN
        elif event.button_name == "btn_printsmth":
            print("something! -- what'd you expect?")