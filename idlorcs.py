import pygame

from settings import Settings
from button import Button
from game_stats import GameStats
import game_functions as gf

def run_game():
    pygame.init()
    pygame.display.set_caption("Idleons")

    # Initialize game objects
    idlorcs_settings = Settings()
    screen = pygame.display.set_mode((idlorcs_settings.screen_width, idlorcs_settings.screen_height))
    stats = GameStats()

    # Create tick event for income every 1 second
    TICKEVENT = pygame.USEREVENT+0
    time_in_ms = 1000
    pygame.time.set_timer(TICKEVENT, time_in_ms)

    # Create the manual button to generate points
    manualclick_button = Button(screen,stats,100,50,400,300,"Get +1 Point")

    # Run game loop
    while True:
        gf.check_events(screen, stats, manualclick_button, TICKEVENT)
        gf.update_screen(idlorcs_settings, screen, stats, manualclick_button)

run_game()
