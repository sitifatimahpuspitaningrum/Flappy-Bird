import pygame

class Bird:
    def __init__(self, x, y, image):
        self.image = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0

    def flap(self):
        self.velocity = -8

    def update(self):
        self.velocity += 0.5
        self.y += self.velocity
        self.rect.centery = self.y

    def draw(self, screen):
        screen.blit(self.image, self.rect)
