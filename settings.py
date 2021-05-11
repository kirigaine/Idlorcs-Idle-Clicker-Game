"""settings.py"""
#from enum import Enum
import pygame

class Settings():

    def __init__(self):
        # Screen settings
        self.screen_width = 800
        self.screen_height = 600
        self.monitor_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self.bg_color = (0,0,0)
        self.particles = []

        print("Monitor Size:" + str(self.monitor_size[0]) + "x" + str(self.monitor_size[1]))
        # Customizable settings
        self.fullscreen = False
        self.screen_resolution = (self.screen_width, self.screen_height)
        self.music_on = True
        self.sound_on = True
        self.music_volume = 0.1
        self.sound_volume = 0.3

# ********* MAYBE REDO THIS AS ENUM LATER ***********
class ScreenResolutions():

    def __init__(self):
        self.resolutions = []
        self.resolutions.append((1920,1080))
        self.resolutions.append((1600,900))
        self.resolutions.append((1440,900))
        self.resolutions.append((1366,768))
        self.resolutions.append((1280,720))
        self.resolutions.append((1024,768))
        self.resolutions.append((800,600))

class MusicPercentBar():
    def __init__(self, parent_button, settings, btn_lower, btn_raise):
        self.current_percent = settings.music_volume
        # ******Might remove display percent entirely, depends if used or not******
        self.display_percent = self.current_percent * 100
        self.parent_button = parent_button
        self.first_button = btn_lower
        self.last_button = btn_raise

        # Position the volume changing arrows as well as the drawn rectangles according to parent button
        self.reposition_children()

    def reposition_children(self):
        """Align all objects to form percent bar"""
        # Iterate through first_buttons's rects and move them to the top and right of parent_button
        for rect in self.first_button.rects:
            rect.topleft = (self.parent_button.rect.right + 5, self.parent_button.rect.top)

        # Iterate through last_button's rects and move them 5 pixels to the right ***CHECK***
        for rect in self.last_button.rects:
            rect.topleft = (rect.left + 5, rect.top)

    def draw(self,screen,settings):
        # Update music volume to current value in settings
        self.current_percent = settings.music_volume
        # Manage raise and lower volume arrows
        self.update_arrows()
        # Set rectangle color to white by default, or gray if parent state is false
        rect_rgb = (255,255,255)
        if not self.get_state():
            rect_rgb = (85,85,85)
        
        # Set base volume of 0.0 and increment it by 0.05 up to current volume to draw x number of rectangles for visual reference
        increment_percent = 0.0
        while(increment_percent != self.current_percent):
            pygame.draw.rect(screen,rect_rgb,pygame.Rect(self.first_button.rect.left+50 + (2*increment_percent*150),self.first_button.rect.top-5, 10, 30))
            # Round to prevent errors
            increment_percent = round(increment_percent+0.05,2)

    def get_state(self):
        # Return state of parent button
        return self.parent_button.toggle_state

    def update_arrows(self):
        # Get current state of parent for comparison
        parentbutton_state = self.get_state()
        # Disable raise and lower volume buttons when parent toggled off
        if not parentbutton_state:
            self.first_button.disable_button()
            self.last_button.disable_button()
        # Disable lower volume button when volume is 0.0
        elif parentbutton_state and self.current_percent == 0.0:
            self.first_button.disable_button()
            self.last_button.enable_button()
        # Disable raise volume button when volume is 1.0
        elif parentbutton_state and self.current_percent == 1.0:
            self.last_button.disable_button()
            self.first_button.enable_button()
        # Enable raise and lower volume buttons when between 0.0 and 1.0
        elif parentbutton_state and self.current_percent > 0.0 and self.current_percent < 1.0:
            self.first_button.enable_button()
            self.last_button.enable_button()

class SoundPercentBar(MusicPercentBar):
    def __init__(self, parent_button, settings, btn_lower, btn_raise):
        super().__init__(parent_button, settings, btn_lower, btn_raise)
        # Change current_percent to manage sound volume rather than music volume
        self.current_percent = settings.sound_volume

    def draw(self,screen,settings):
        # Had to override this method due to implementation, prevents from having to pass more variables to here
        # Update sound volume to current value in settings
        self.current_percent = settings.sound_volume
        # Manage raise and lower volume arrows
        self.update_arrows()
        # Set rectangle color to white by default, or gray if parent state is false
        text_rgb = (255,255,255)
        if not self.get_state():
            text_rgb = (85,85,85)
        
        # Set base volume of 0.0 and increment it by 0.05 up to current volume to draw x number of rectangles for visual reference
        increment_percent = 0.0
        while(increment_percent != self.current_percent):
            pygame.draw.rect(screen,text_rgb,pygame.Rect(self.first_button.rect.left+50 + (2*increment_percent*150),self.first_button.rect.top-5, 10, 30))
            # Round to prevent errors
            increment_percent = round(increment_percent+0.05,2)


class SoundHandler():
    """A class to handle sound"""
    def __init__(self, game_settings):
        # Pull in initial values from game_settings
        self.sound_volume = game_settings.sound_volume
        self.sound_on = game_settings.sound_on

    def lower_volume(self, game_settings):
        # If volume is greater than 0.0, lower by 0.05 and call set_volume
        if self.sound_volume > 0.0:
            self.sound_volume = round(self.sound_volume - 0.05, 3)
            self.set_volume(game_settings)

    def raise_volume(self, game_settings):
        # If volume is less than 1.0, raise by 0.05 and call set_volume
        if self.sound_volume < 1.0:
            self.sound_volume = round(self.sound_volume + 0.05,3)
            self.set_volume(game_settings)
    
    def set_volume(self, game_settings):
        # Copy self.sound_volume to game_settings.sound_volume
        game_settings.sound_volume = self.sound_volume


class MusicHandler():
    """A class to play and toggle music"""

    def __init__(self, game_settings):

        self.music_volume = game_settings.music_volume
        pygame.mixer.music.load("music\\Prelude1inCmajor.flac")
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(-1)
        self.music_on = game_settings.music_on
        self.music_playing = True

    def toggle(self, game_settings):
        """Toggles music off/on based on current state"""
        self.music_on = game_settings.music_on
        if self.music_on:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

    def pause_unpause(self):
        if self.music_playing:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
        self.music_playing = not self.music_playing

    def restart(self):
        if self.music_volume > 0.0:
            pygame.mixer.music.play(-1)
            self.music_on = True

    def lower_volume(self, game_settings):
        if self.music_volume > 0.0:
            self.music_volume = round(self.music_volume-0.05,3)
            self.set_volume(game_settings)

    def raise_volume(self, game_settings):
        if self.music_volume < 1.0:
            self.music_volume = round(self.music_volume+0.05,3)
            self.set_volume(game_settings)

    def set_volume(self, game_settings):
        game_settings.music_volume = self.music_volume
        pygame.mixer.music.set_volume(game_settings.music_volume)
        if not self.music_on and self.music_volume > 0.0:
            self.toggle(game_settings)