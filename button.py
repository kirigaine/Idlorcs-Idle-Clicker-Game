import pygame.freetype
from pygame.sprite import Sprite

def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    font = pygame.freetype.SysFont("Courier", font_size, bold = True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()

class Button(Sprite):
    def __init__(self, name, center_position, text, font_size, bg_rgb, text_rgb, action=None):

        super().__init__()

        self.name = name
        self.mouse_over = False
        self.hover_sound = pygame.mixer.Sound('sounds\\click.wav')
        self.hover_sound.set_volume(0.3)
        self.already_clicked = False

        default_image = create_surface_with_text(text, font_size, text_rgb, bg_rgb)
        highlighted_image = create_surface_with_text(text, font_size * 1.2, text_rgb, bg_rgb)

        self.images = [default_image, highlighted_image]
        self.rects = [default_image.get_rect(center=center_position), highlighted_image.get_rect(center=center_position)]

        self.action = action

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if not self.already_clicked:
                self.hover_sound.play()
                self.already_clicked = True
            if mouse_up: return self.action
        else:
            self.mouse_over = False
            self.already_clicked = False

    def drawblit(self, surface):
        surface.blit(self.image, self.rect)

    def checkClick(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            if self.action is not None:
                pygame.event.post(pygame.event.Event(int(self.action),{ "button_name" : self.name }))
                return True
        return False