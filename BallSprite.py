"""
BallSprite.py - Sprite class for a ball that bounces
Jade Harbert
CSC 235
5-18-21
"""
import pygame
from random import randint
from pygame import Vector2

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRAVITY = 0
SCALE_FACTOR = 4

# Initializes base elements

pygame.mixer.init()

bouncing_sound = pygame.mixer.Sound("Sounds/Bouncing_Ball.wav")
bouncing_sound.set_volume(0.5)
life_loss_sound = pygame.mixer.Sound("Sounds/Lost-life-sound-effect.wav")
life_loss_sound.set_volume(0.075)


class BallSprite(pygame.sprite.Sprite):

    def __init__(self, image):

        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        # Scales the image down to an appropriate size
        self.image = pygame.transform.scale(self.image, (self.rect.w // SCALE_FACTOR, self.rect.h // SCALE_FACTOR))
        self.rect = self.image.get_rect()

        self.rect.center = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2

        # Sets the velocity to a random vector between the ints
        self.vel = Vector2(randint(-300, -250), randint(250, 300))
        self.player1_score = 0
        self.player2_score = 0

    def update(self, secs):

        self.vel.y += GRAVITY * secs
        r = self.rect
        r.x += self.vel.x * secs
        r.y += self.vel.y * secs

        # If the sprite goes off the edge of the screen,
        # make it move in the opposite direction
        if r.right > SCREEN_WIDTH:
            self.vel.x = -abs(self.vel.x)
            r.right = SCREEN_WIDTH
            bouncing_sound.play()
        elif r.left < 0:
            self.vel.x = abs(self.vel.x)
            r.left = 0
            bouncing_sound.play()

        # If the sprite goes in player 1's goal, add a point to player 2,
        # respawn the ball, and play the loss life sound
        if r.bottom > SCREEN_HEIGHT:
            self.vel.y = 0
            self.vel.x = 0
            r.center = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
            life_loss_sound.play()
            self.player2_score += 1
            self.play()
        # If the sprite goes in player 2's goal, add a point to player 1,
        # respawn the ball, and play the loss life sound
        elif r.top < 0:
            self.vel.y = 0
            self.vel.x = 0
            r.center = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
            life_loss_sound.play()
            self.player1_score += 1
            self.play()

    # Function responsible for collision on the paddle
    def collision(self, player_top, player1):

        if player1:
            self.rect.bottom = player_top
            self.vel.y = -abs(self.vel.y) * 1.03
        else:
            self.rect.top = player_top
            self.vel.y = abs(self.vel.y) * 1.03
        bouncing_sound.play()

    # Function responsible for respawning the ball
    def play(self):
        self.vel = Vector2(randint(-350, -150), randint(350, 400))

    # Function responsible for getting the scores
    def get_scores(self):
        return self.player1_score, self.player2_score
