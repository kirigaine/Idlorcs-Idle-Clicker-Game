import pygame
from random import randint, choice

WHITE = (255, 255, 255)

"""
class Particle():
    def __init__(self, screen):
        # Snow particles for the menu
        self.screen_rect = screen.get_rect()
        # location = (location_x, location_y)
        # location[0] = location_x, location[1] = location_y
        self.location = (randint(0, self.screen_rect.width),0)
        # velocity = (velocity_x, velocity_y)
        # velocity[0] = velocity_x, velocity[1] = velocity_y
        self.velocity = ((randint(-2,2))/6, 1/(randint(2,3)))

    def draw(self, screen):
        #Draw the particle as well as perform changes to location and velocity for next draw
        pygame.draw.circle(screen, WHITE, (self.location), 1)
        self.location = (self.location[0] + self.velocity[0], self.location[1] + self.velocity[1])
        velocity_change = (0.01 * choice([i for i in range(-1,2) if i not in [0]]))
        self.velocity = (self.velocity[0] + velocity_change, self.velocity[1])
"""

class Particle():
    def __init__(self, screen, location, velocity):
        """Snow particles for the menu"""
        self.screen_rect = screen.get_rect()
        # location = (location_x, location_y)
        self.location = location
        # velocity = (velocity_x, velocity_y)
        self.velocity = velocity

    def draw(self, screen):
        """Draw the particle as well as perform changes to location and velocity for next draw"""
        pygame.draw.circle(screen, WHITE, (self.location), 1)
        self.location = (self.location[0] + self.velocity[0], self.location[1] + self.velocity[1])

class SnowParticle(Particle):
    """Snow particles for the menu"""
    def __init__(self, screen):
        super(SnowParticle).__init__()
        self.screen_rect = screen.get_rect()
        # location = (location_x, location_y)
        # location[0] = location_x, location[1] = location_y
        self.location = (randint(0, self.screen_rect.width),0)
        # velocity = (velocity_x, velocity_y)
        # velocity[0] = velocity_x, velocity[1] = velocity_y
        self.velocity = ((randint(-2,2))/6, 1/(randint(2,3)))

    def draw(self, screen):
        """Draw the snow particle as well as perform changes to location and velocity for next draw"""
        pygame.draw.circle(screen, WHITE, (self.location), 1)
        self.location = (self.location[0] + self.velocity[0], self.location[1] + self.velocity[1])
        velocity_change = (0.01 * choice([i for i in range(-1,2) if i not in [0]]))
        self.velocity = (self.velocity[0] + velocity_change, self.velocity[1])



