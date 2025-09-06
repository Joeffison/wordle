import abc

import pygame


class BaseComponent(abc.ABC):
    def __init__(self, width, height, background_color):
        self.width = width
        self.height = height
        self.background_color = background_color
        self._surface = None

    @property
    def size(self):
        return self.width, self.height

    @property
    def surface(self):
        if not self._surface:
            self._surface = pygame.Surface(self.size)

        return self._surface

    def draw(self):
        self.draw_background()

    def draw_background(self, rect=None):
        self.surface.fill(self.background_color, rect)
