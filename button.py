"""button.py"""
import pygame.freetype
from pygame.sprite import Sprite

def create_text(text, font_size, text_rgb, bg_rgb):
    font = pygame.freetype.SysFont("Courier", font_size, bold = True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()

class Button(Sprite):
    def __init__(self, name, center_position, text, font_size, bg_rgb, text_rgb, settings, action=None, topleft=None):

        super().__init__()

        self.name = name
        self.enabled = True
        self.mouse_over = False
        self.hover_sound = pygame.mixer.Sound('sounds\\click.wav')
        self.hover_sound.set_volume(settings.sound_volume)
        self.already_clicked = False

        default_image = create_text(text, font_size, text_rgb, bg_rgb)
        highlighted_image = create_text(text, font_size * 1.2, (255,0,0), bg_rgb)
        disabled_image = create_text(text, font_size, (100,100,100), bg_rgb)
        self.images = [default_image, highlighted_image, disabled_image]
        if topleft is None:
            self.rects = [default_image.get_rect(center=center_position), highlighted_image.get_rect(center=center_position), disabled_image.get_rect(center=center_position)]
        else:
            self.rects = [default_image.get_rect(topleft=topleft), highlighted_image.get_rect(topleft=topleft)]
            pass # TODO
        self.action = action

    @property
    def image(self):
        if not self.enabled:
            return self.images[2]
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up, settings):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if not self.already_clicked and self.enabled:
                if settings.sound_on:
                    self.hover_sound.set_volume(settings.sound_volume)
                    self.hover_sound.play()
                self.already_clicked = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False
            self.already_clicked = False

    def disable_button(self):
        self.enabled = False

    def enable_button(self):
        self.enabled = True

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def checkClick(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            if self.action is not None and self.enabled:
                pygame.event.post(pygame.event.Event(int(self.action),{ "button_name" : self.name }))
                return True
        return False

class ToggleButton(Button):
    def __init__(self, name, center_position, text, font_size, bg_rgb, text_rgb, settings, toggle_state=False, action=None, topleft=None):
        super().__init__(name, center_position, text, font_size, bg_rgb, text_rgb, settings, action, topleft)
        self.toggle_state = toggle_state

        default_offimage = create_text(text+" [ ]:",font_size,text_rgb,bg_rgb)
        highlighted_offimage = create_text(text+" [ ]:",font_size,(255,0,0),bg_rgb)
        default_onimage = create_text(text+" [X]:",font_size,text_rgb,bg_rgb)
        highlighted_onimage = create_text(text+" [X]:",font_size,(255,0,0),bg_rgb)

        self.images = [default_offimage, highlighted_offimage, default_onimage, highlighted_onimage]
        if topleft is None:
            self.rects = [default_offimage.get_rect(center=center_position), highlighted_offimage.get_rect(center=center_position),
            default_onimage.get_rect(center=center_position), highlighted_onimage(center=center_position)]
        else:
            self.rects = [default_offimage.get_rect(topleft=topleft), highlighted_offimage.get_rect(topleft=topleft),
            default_onimage.get_rect(topleft=topleft), highlighted_onimage.get_rect(topleft=topleft)]
            pass # TODO

    @property
    def image(self):
        if not self.mouse_over and not self.toggle_state:
            return self.images[0] 
        elif self.mouse_over and not self.toggle_state:
            return self.images[1] 
        elif not self.mouse_over and self.toggle_state:
            return self.images[2] 
        elif self.mouse_over and self.toggle_state:
            return self.images[3]

    @property
    def rect(self):
        if not self.mouse_over and not self.toggle_state:
            return self.rects[0] 
        elif self.mouse_over and not self.toggle_state:
            return self.rects[1] 
        elif not self.mouse_over and self.toggle_state:
            return self.rects[2] 
        elif self.mouse_over and self.toggle_state:
            return self.rects[3] 

    def toggle(self):
        self.toggle_state = not self.toggle_state
        
    def checkClick(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            if self.action is not None:
                pygame.event.post(pygame.event.Event(int(self.action),{ "button_name" : self.name }))
                self.toggle()
                return True
        return False
        