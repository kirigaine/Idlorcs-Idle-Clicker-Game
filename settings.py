import pygame

class Settings():

    def __init__(self):
        # Screen settings
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (0,0,0)

        # Customizable settings
        self.music_on = True
        self.sound_on = True
        self.music_volume = 0.1
        self.sound_volume = 0.3

class PercentBar():
    def __init__(self, label, starting_percent, is_on, btn_lower, btn_raise, center_position, top=None, bottom=None, left=None, right=None):
        self.current_percent = starting_percent
        self.display_percent = self.current_percent * 100
        self.label = label
        self.on = is_on
        self.rect = pygame.Rect(0, 0, 200, 50)

        if top is None and bottom is None and left is None and right is None:
            self.rect.center = center_position
        else:
            self.rect.top = top
        btn_lower.rect.right = self.rect.left
        btn_raise.rect.left = self.rect.right

    def draw(self):
        pass

class MusicHandler():
    """A class to play and toggle music"""

    def __init__(self, game_settings):

        self.music_volume = game_settings.music_volume
        pygame.mixer.music.load("music\\Prelude1inCmajor.flac")
        pygame.mixer.music.set_volume(self.music_volume)
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

    def lower_volume(self):
        pass # TODO
    def raise_volume(self):
        pass # TODO