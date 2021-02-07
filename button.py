import pygame.font
class Button():

    def __init__(self, screen, stats, x_size, y_size, x_pos, y_pos, msg):
        
        # Reference screen locally
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Button dimensions/properties
        self.width = x_size
        self.height = y_size
        self.button_color = (255, 0, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 24)

        # Create rect for button
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x_pos, y_pos)

        # Call to render 
        self.render_label(msg)

    def render_label(self, msg):
        # Render text and place its rect at center of button rect
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Add button and text to screen
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)