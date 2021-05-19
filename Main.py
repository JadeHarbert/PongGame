"""
Main.py - Driver for Insane Asylum Pong
Jade Harbert
CSC 235
5-18-21
"""
import pygame
from pygame.locals import *
from BallSprite import BallSprite
from PlayerSprite import PlayerSprite

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
font_name = pygame.font.match_font('arial')
BLACK = (0, 0, 0)


# Function that simplifies drawing text on a screen\
def draw_text(surface, text, size, temp_x, temp_y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (temp_x, temp_y)
    surface.blit(text_surface, text_rect)


# Function that displays the start screen and is responsible
# for handling the events on the start screen
def start_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "Insane Asylum Pong!", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
    draw_text(screen, "Arrow keys move Player1, A/D keys move Player 2", 22,
              SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    draw_text(screen, "Press a key to begin", 18, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
            if e.type == pygame.KEYUP:
                waiting = False


# Function that is responsible for displaying the end screen
# and is responsible for handling the events on the end screen
def end_screen(winner):
    screen.blit(background, background_rect)
    draw_text(screen, "Thank you for Playing!", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
    draw_text(screen, winner + " wins!", 22,
              SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    draw_text(screen, "Press a key to quit", 18, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
            if e.type == pygame.KEYUP:
                pygame.quit()
                waiting = False
                quit()


# Initializes and sets up the base elements
BACKGROUND_FILENAME = "Images/Padded_Room_Resized.jpg"
BALL_FILENAME = "Images/TennisBall_Resized.png"

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("Sounds/Arcade_Kid.mp3")
pygame.mixer.music.set_volume(0.20)
pygame.mixer.music.play(loops=-1)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption("Insane Asylum Pong")

background = pygame.image.load(BACKGROUND_FILENAME).convert()
background_rect = background.get_rect()

ball_image = pygame.image.load(BALL_FILENAME).convert_alpha()
clock = pygame.time.Clock()

# Creates a group responsible for the ball
ball_group = pygame.sprite.Group()
ball = BallSprite(ball_image)
ball_group.add(ball)

# Creates groups responsible for player1 and player2 paddles
player_group = pygame.sprite.Group()
player2_group = pygame.sprite.Group()
player = PlayerSprite(SCREEN_HEIGHT - 50)
player2 = PlayerSprite(50)
player_group.add(player)
player2_group.add(player2)

x, y, move_x, move_y = 0, 0, 0, 0
movement = 5
player1_score, player2_score = 0, 0
temp_score1, temp_score2 = 0, 0
winning_score = 7

is_start_screen = True

while True:
    # Displays the start screen and initially displays the score
    if is_start_screen:
        start_screen()
        is_start_screen = False
        screen.blit(background, (0, 0))
        draw_text(screen, str(player1_score), 30, 50, 15)
        draw_text(screen, str(player2_score), 30, SCREEN_WIDTH - 50, 15)

    else:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

        time_passed = clock.tick(60)
        time_passed_seconds = time_passed / 1000.0

        # Clears the groups
        ball_group.clear(screen, background)
        player_group.clear(screen, background)
        player2_group.clear(screen, background)

        # Updates all of the groups
        ball_group.update(time_passed_seconds)
        player_group.update(pygame.K_LEFT, pygame.K_RIGHT, time_passed_seconds)
        player2_group.update(pygame.K_a, pygame.K_d, time_passed_seconds)

        # Draws all of the groups to the screen
        ball_group.draw(screen)
        player_group.draw(screen)
        player2_group.draw(screen)

        player1_score, player2_score = ball.get_scores()

        # Displays the scores if they have changed
        if player1_score != temp_score1 or player2_score != temp_score2:
            screen.blit(background, background_rect)
            temp_score1 = player1_score
            temp_score2 = player2_score
            draw_text(screen, str(player1_score), 30, 50, 15)
            draw_text(screen, str(player2_score), 30, SCREEN_WIDTH - 50, 15)

        # Responsible for hits to player 1 paddle
        hits = pygame.sprite.groupcollide(ball_group, player_group, False, False)
        for hit in hits:
            hit.collision(player.rect.top, True)

        # Responsible for hits to player 2 paddle
        hits = pygame.sprite.groupcollide(ball_group, player2_group, False, False)
        for hit in hits:
            hit.collision(player2.rect.bottom, False)

        pygame.display.update()

        # Determines if the winning score has been reached
        # and displays the end screen for that player
        if player1_score == winning_score:
            end_screen("Player1")
        elif player2_score == winning_score:
            end_screen("Player2")
