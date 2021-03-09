"""sets.py"""
import particles
#class BasicSet:
 #   def __init__(self, *individuals):
  #      self.individuals = list(individuals)
#
 #   def draw(self, screen):
  #      for individual in self.individuals:
   #      screen.blit(individual.image, individual.rect)

class ButtonSet():
    def __init__(self, *buttons):
        self.buttons = list(buttons)

    def addButton(self, newbutton):
        if (newbutton not in self.buttons):
            self.buttons.append(newbutton)

    def anyClicked(self, click_location):
        for button in self.buttons:
            button.checkClick(click_location)

    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen)

class ScreenSet():
    def __init__(self, *items):
        self.items = list(items)

    def draw(self, screen):
        for item in self.items:
            item.draw(screen)

class PercentSet():
    def __init__(self, *percentbars):
        self.percentbars = list(percentbars)

    def draw(self, screen, settings):
        for percentbar in self.percentbars:
            percentbar.draw(screen, settings)

class SnowParticleSet():
    
    def __init__(self, *particles):
        self.particles = list(particles)

    def add_particles(self, screen):
        if len(self.particles) <= 500:
            self.particles.append(particles.SnowParticle(screen))

    def update(self, screen):
        self.add_particles(screen)
        for particle in self.particles:
            particle.draw(screen)
            if particle.location[0] < 0 or particle.location[0] > screen.get_rect().width or particle.location[1] > screen.get_rect().height:
                self.particles.remove(particle)