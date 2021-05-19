"""
PlayerSprite.py - Sprite class for a paddle used in Pong
Jade Harbert
CSC 235
5-18-21
"""
import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480


class PlayerSprite(pygame.sprite.Sprite):

    def __init__(self, height):
        super().__init__()

        self.image = pygame.Surface((75, 10))
        self.rect = self.image.get_rect()
        self.rect.center = SCREEN_WIDTH / 2, height
        self.speed_x = 0
        self.score = 0

    # Function updates the paddle based on the keys passed in and
    # on how many secs were passed in
    def update(self, left_key, right_key, secs):
        self.speed_x = 0
        vel = 800
        keys = pygame.key.get_pressed()

        if keys[left_key]:
            self.speed_x = -(vel * secs)
        elif keys[right_key]:
            self.speed_x = (vel * secs)

        self.rect.x += self.speed_x

        # Responsible for making sure the paddle doesn't go off the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
