import pygame
import math

class Pipe:
    def __init__(self, x, height, image_top, image_bottom, gap, night_mode=False):
        self.pipe_top = image_top
        self.pipe_bottom = image_bottom
        self.x = x
        self.base_height = height
        self.gap = gap
        self.night_mode = night_mode
        self.scored = False  

        self.offset = 0
        self.direction = 1
        self.speed = 0.5

        self.update_rects() 
    
    def update_rects(self):
        self.top = self.base_height - self.pipe_top.get_height() + self.offset
        self.bottom = self.base_height + self.gap + self.offset
        self.top_rect = self.pipe_top.get_rect(topleft=(self.x, self.top))
        self.bottom_rect = self.pipe_bottom.get_rect(topleft=(self.x, self.bottom))

    def move(self):
        self.x -= 2
        if self.night_mode:
            self.offset += self.speed * self.direction
            if self.offset > 20 or self.offset < -20:
                self.direction *= -1
        self.update_rects()

    def draw(self, screen):
        screen.blit(self.pipe_top, (self.x, self.top))
        screen.blit(self.pipe_bottom, (self.x, self.bottom))