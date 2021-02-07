import sys
from math import floor

import pygame
import pygame.font

# Check for player input
def check_events(screen, stats, testbutton, TICKEVENT):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == TICKEVENT: 
            update_currency(stats)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_buttons(screen, stats, testbutton, mouse_x, mouse_y)

# Determine which buttons were pressed to determine function
def check_buttons(screen, stats, testbutton, mouse_x, mouse_y):
    if testbutton.rect.collidepoint(mouse_x, mouse_y):
        stats.manual_clicks+=1
        stats.rock_currency+=1

# Draw current screen
def update_screen(idlorcs_settings, screen, stats, manualclick_button):
    # Set screen color, add objects and draw
    screen.fill(idlorcs_settings.bg_color)
    manualclick_button.draw_button()
    renderdraw_currency(screen, stats)
    pygame.display.flip()

def update_currency(stats):
    # Summation of all producers and their upgrade multiplier into total currency
    total_to_add = 0
    total_to_add += (stats.snorckyjr_count * stats.snorckyjr_mult)
    total_to_add += (stats.hork_count * stats.hork_mult)
    total_to_add += (stats.pork_count * stats.pork_mult)
    total_to_add += (stats.gork_count * stats.gork_mult)
    total_to_add += (stats.snorck_count * stats.snorck_mult)
    stats.rock_currency += total_to_add

# Render and draw currency in fixed location
def renderdraw_currency(screen, stats):
    font = pygame.font.SysFont(None, 24)
    msg_image = font.render(str(floor(stats.rock_currency)), True, (0,0,0))
    msg_image_rect = msg_image.get_rect()
    msg_image_rect.center = (400,250)
    screen.blit(msg_image, msg_image_rect)