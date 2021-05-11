"""
*********************************************************
*                                                       *
* Project Name: Idlorcs                                 *
* Author: github.com/kirigaine                          *
* Description: An idle game based around orcs           *
* Requirements: pip install -r requirements.txt         *
*                                                       *
*********************************************************
"""
import sys
import pygame
import pygame.freetype

import button as uibtn
import game_functions as gf
import game_statistics as gs
import sets
import settings
import uielements as gui

def main():
    """Main logic loop of application"""

    # Declare game active boolean to manage our gamestate loop
    game_active = True

    # Initialize and manage pygame settings
    pygame.init()
    pygame.display.set_caption("Idlorcs")

    # Instantiate game settings
    game_settings = settings.Settings()
    game_stats = gs.GameStats()

    # Initialize music handler
    bg_music = settings.MusicHandler(game_settings)
    bg_sound = settings.SoundHandler(game_settings)

    # Declare our screen and choose titlescreen game_state to initially display
    screen = pygame.display.set_mode((game_settings.screen_width,game_settings.screen_height))
    game_state = gf.GameState.TITLESCREEN

    # Loop gamestates while active, manage music and particles if in menu or in game
    while game_active:
        if game_state == gf.GameState.TITLESCREEN:
            game_state = title_screen(screen, bg_music, bg_sound, game_settings, game_settings.particles)
        elif game_state == gf.GameState.GAME:
            # Remove all particles from particle list, and pause the music if music is enabled.
            # Then transition game_state. Reverse all if exiting gamestate
            game_settings.particles = None
            if bg_music.music_playing and game_settings.music_on:
                bg_music.pause_unpause()
            game_state = game_screen(screen, bg_music, bg_sound, game_settings)
            game_settings.particles = []
            if not bg_music.music_playing and game_settings.music_on:
                bg_music.pause_unpause()
        elif game_state == gf.GameState.SETTINGS:
            game_state = settings_screen(screen, bg_music, bg_sound, game_settings, game_settings.particles)
        elif game_state == gf.GameState.QUIT:
            game_active = False

    # Close pygame upon exiting of gamestate loop -- quit the program
    pygame.quit()
    sys.exit()

def title_screen(screen, music, sound, g_settings, particles):
    """Initialize buttons for title screen, put into button set to handle as a whole and direct towards game loop"""
    # Get screen rect to position ui
    screen_rect = screen.get_rect()

    # Initialize title screen buttons and buttonset
    btn_playgame = uibtn.Button("btn_playgame",(screen_rect.centerx,400),"Play",30,gui.BLACK,gui.WHITE,g_settings,gf.ButtonEvent.MENU_BUTTON)
    btn_settings = uibtn.Button("btn_settings",(screen_rect.centerx,450),"Settings",30,gui.BLACK,gui.WHITE,g_settings,gf.ButtonEvent.MENU_BUTTON)
    btn_quitgame = uibtn.Button("btn_quitgame",(screen_rect.centerx,500),"Quit",30,gui.BLACK,gui.WHITE,g_settings,gf.ButtonEvent.MENU_BUTTON)
    btn_github = uibtn.Button("btn_github",(screen.get_rect().right-120, screen.get_rect().bottom-15),"Created By: Kirigaine",15,gui.BLACK,gui.WHITE,g_settings,gf.ButtonEvent.MENU_BUTTON)
    btn_music = uibtn.Button("btn_music",(screen.get_rect().left+135, screen.get_rect().bottom-15),"Music By: Steven O'Brien",15,gui.BLACK,gui.WHITE,g_settings,gf.ButtonEvent.MENU_BUTTON)
    btns_titlescreen = sets.ButtonSet(btn_playgame, btn_settings, btn_quitgame, btn_github, btn_music)

    # Initialize title screen images and imageset
    img_logo = gui.MyImage(screen, 'images\\idlorcstemplogo.png')
    itms_titlescreen = sets.ScreenSet(img_logo)

    return game_loop(screen, btns_titlescreen, itms_titlescreen, music, sound, g_settings, particles)

def settings_screen(screen, music, sound, g_settings, particles):
    """Initialize buttons for setting screen, put into button set to handle as a whole and direct towards game loop"""

    # Get screen rect to position ui
    screen_rect = screen.get_rect()

    # Initialize settings screen buttons and buttonset
    btn_return = uibtn.Button("btn_return",(screen_rect.centerx,screen_rect.bottom-100),"Return",30,gui.BLACK,gui.WHITE,g_settings,gf.ButtonEvent.MENU_BUTTON)
    btn_fullscreentoggle = uibtn.ToggleButton("btn_fullscreentoggle",(0,300),"Fullscreen",30,gui.BLACK,gui.WHITE,g_settings,g_settings.fullscreen,gf.ButtonEvent.MENU_BUTTON,topleft=(screen_rect.width/8,100))
    btn_musictoggle = uibtn.ToggleButton("btn_musictoggle",(screen_rect.left,400),"Music",30,gui.BLACK,gui.WHITE,g_settings,g_settings.music_on,gf.ButtonEvent.MENU_BUTTON,topleft=(screen_rect.width/8,200))
    btn_soundtoggle = uibtn.ToggleButton("btn_soundtoggle",(100,500),"Sound",30,gui.BLACK,gui.WHITE,g_settings,g_settings.sound_on,gf.ButtonEvent.MENU_BUTTON,topleft=(screen_rect.width/8,300))
    btn_lowermusic = uibtn.Button("btn_lowermusic",(250,200),"<",30,gui.BLACK,gui.WHITE,g_settings,gf.ButtonEvent.MENU_BUTTON,topleft=(screen_rect.width/8+200,200))
    btn_raisemusic = uibtn.Button("btn_raisemusic",(300,200),">",30,gui.BLACK,gui.WHITE,g_settings,gf.ButtonEvent.MENU_BUTTON,topleft=(screen_rect.width/8+550,200))
    btn_lowersound = uibtn.Button("btn_lowersound",(0,0),"<",30,gui.BLACK,gui.WHITE,g_settings,gf.ButtonEvent.MENU_BUTTON,topleft=(300,300))
    btn_raisesound = uibtn.Button("btn_raisesound",(0,0),">",30,gui.BLACK,gui.WHITE,g_settings,gf.ButtonEvent.MENU_BUTTON,topleft=(650,300))
    btns_settingsscreen = sets.ButtonSet(btn_return, btn_fullscreentoggle, btn_musictoggle, btn_soundtoggle, btn_lowermusic, btn_raisemusic, btn_lowersound, btn_raisesound)

    pb_music = settings.MusicPercentBar(btn_musictoggle, g_settings, btn_lowermusic, btn_raisemusic)
    pb_sound = settings.SoundPercentBar(btn_soundtoggle, g_settings, btn_lowersound, btn_raisesound)
    pbs_settingscreen = sets.PercentSet(pb_music, pb_sound)

    # Initialize settings screen images and imageset
    itms_settingsscreen = sets.ScreenSet()

    return game_loop(screen, btns_settingsscreen, itms_settingsscreen, music, sound, g_settings, particles, pbs_settingscreen)

def game_screen(screen, music, sound, g_settings):
    """Initialize buttons for game screen, put into button set to handle as a whole and direct towards game loop"""
    # Get screen rect to position ui
    screen_rect = screen.get_rect()

    # Initialize game screen buttons and buttonset
    btn_titlescreen = uibtn.Button("btn_titlescreen",(0,0),"Return",30,gui.BLACK,gui.WHITE,g_settings,gf.ButtonEvent.MENU_BUTTON,topleft=screen_rect.topleft)
    btn_printsmth = uibtn.Button("btn_printsmth",(400,400),"Print Something",30,gui.BLACK,gui.WHITE,g_settings,gf.ButtonEvent.MENU_BUTTON)
    btns_gamescreen = sets.ButtonSet(btn_titlescreen, btn_printsmth)

    # Initialize game screen images and imageset
    gui_buymenu = gui.SubMenu(screen)
    itms_gamescreen = sets.ScreenSet(gui_buymenu)

    return game_loop(screen, btns_gamescreen, itms_gamescreen, music, sound, g_settings)

def game_loop(screen, buttons, items, music, sound, g_settings, particles=None, percentthing=None):
    """Manage events, return a gamestate change if it happens, and update the screen"""
    while True:
        # Check and manage event queue
        gs_change = gf.check_events(buttons, music, sound, g_settings)
        # If we are returned a new gamestate from checking events, return the gamestate again to transition
        if isinstance(gs_change, gf.GameState):
            return gs_change

        # Update all aspects on screen
        gf.update_screen(screen, buttons, items, g_settings, particles, percentthing)

# Call to main program loop
main()
