# Stephen Lee
# 9/18/19
# Pong

import pygame
import sys
import pygame.math
import random
from pygame.locals import *

# global variables
# window size
WINDOWWIDTH = 800
WINDOWHEIGHT = 400

# speed of game
SPEED = 4

# horizontal paddle size
# for vertical, the width and height will be swapped
HPADDLEWIDTH = 120
HPADDLEHEIGHT = 20
VPADDLEWIDTH = 20
VPADDLEHEIGHT = 120

# ball size and initial position
RADIUS = 10

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
YELLOW = (255, 255, 0)

def draw_text(text, font, surface, x, y):
    textobj = font.render(text, True, WHITE, BLACK)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# class paddle
class Paddle:
    # rect is a rectangle
    def __init__(self, rect, scale=1):
        self.rect_ = pygame.Rect(rect)
        self.scale_ = scale

    def __str__(self):
        return 'Paddle: rect={}'.format(self.rect_)

    def get_rect(self):
        return self.rect_

    def move_up(self):
        self.rect_.top -= self.scale_

    def move_down(self):
        self.rect_.top += self.scale_

    def move_left(self):
        self.rect_.left -= self.scale_

    def move_right(self):
        self.rect_.right += self.scale_

# set up pygame
pygame.init()
clock = pygame.time.Clock()
surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Pong')

# font
default_font = pygame.font.SysFont(None, 20)

# sounds
bounce = pygame.mixer.Sound('sound/bounce.wav')
losegame = pygame.mixer.Sound('sound/losegame.wav')
wingame = pygame.mixer.Sound('sound/wingame.wav')
losematch = pygame.mixer.Sound('sound/losematch.wav')
winmatch = pygame.mixer.Sound('sound/winmatch.wav')

# images
paddleimage = pygame.image.load('images/paddle.png')
horizontalimage = pygame.transform.scale(paddleimage, (HPADDLEWIDTH, HPADDLEHEIGHT))
verticleimage = pygame.transform.scale(paddleimage, (VPADDLEWIDTH, VPADDLEHEIGHT))

# default scores
player_score = 0
computer_score = 0
player_match = 0
computer_match = 0
points_needed = 11

# loop variables
play_again = True

# run game loop
while play_again:
    # set up start of game
    # movement variables
    move_left = False
    move_right = False
    move_up = False
    move_down = False

    # create objects
    # 6 paddles
    cside = Paddle(rect=(0, (WINDOWHEIGHT - VPADDLEHEIGHT) / 2, VPADDLEWIDTH, VPADDLEHEIGHT), scale=SPEED)
    ctop = Paddle(rect=((WINDOWWIDTH / 4) - (HPADDLEWIDTH / 2), 0, HPADDLEWIDTH, HPADDLEHEIGHT), scale=SPEED)
    cbot = Paddle(
        rect=((WINDOWWIDTH / 4) - (HPADDLEWIDTH / 2), WINDOWHEIGHT - HPADDLEHEIGHT, HPADDLEWIDTH, HPADDLEHEIGHT),
        scale=SPEED)
    pside = Paddle(
        rect=(WINDOWWIDTH - VPADDLEWIDTH, (WINDOWHEIGHT - VPADDLEHEIGHT) / 2, VPADDLEWIDTH, VPADDLEHEIGHT),
        scale=SPEED)
    ptop = Paddle(rect=((WINDOWWIDTH * 3 / 4) - (HPADDLEWIDTH / 2), 0, HPADDLEWIDTH, HPADDLEHEIGHT), scale=SPEED)
    pbot = Paddle(rect=(
    (WINDOWWIDTH * 3 / 4) - (HPADDLEWIDTH / 2), WINDOWHEIGHT - HPADDLEHEIGHT, HPADDLEWIDTH, HPADDLEHEIGHT),
                  scale=SPEED)

    # ball position
    # default is middle of screen
    ballx = WINDOWWIDTH / 2
    bally = WINDOWHEIGHT / 2

    # random velocity
    velx = random.randint(-5, 6)
    vely = random.randint(-5, 6)
    ball_speed = random.randint(1, 11)

    # group horizontal paddles
    hpaddles = [ctop, cbot, ptop, pbot]

    # group vertical paddles
    vpaddles = [cside, pside]

    gameover = False
    while not gameover:
        # check for events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                # Change the keyboard variables.
                if event.key == K_LEFT:
                    move_right = False
                    move_left = True
                if event.key == K_RIGHT:
                    move_left = False
                    move_right = True
                if event.key == K_UP:
                    move_down = False
                    move_up = True
                if event.key == K_DOWN:
                    move_up = False
                    move_down = True
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_LEFT:
                    move_left = False
                if event.key == K_RIGHT:
                    move_right = False
                if event.key == K_UP:
                    move_up = False
                if event.key == K_DOWN:
                    move_down = False

        # Move player paddle.
        # Up and down moves the side paddle
        # Left and right moves the top and bottom paddles
        if move_down and pside.get_rect().bottom < WINDOWHEIGHT:
            pside.move_down()
        if move_up and pside.get_rect().top > 0:
            pside.move_up()
        if move_left and ptop.get_rect().left > WINDOWWIDTH / 2:
            ptop.move_left()
            pbot.move_left()
        if move_right and ptop.get_rect().right < WINDOWWIDTH:
            ptop.move_right()
            pbot.move_right()

        # Computer moves.
        # moves based on center position of ball
        if cside.get_rect().centery < bally and cside.get_rect().bottom <= WINDOWHEIGHT:
            cside.move_down()
        if cside.get_rect().centery > bally and cside.get_rect().top >= 0:
            cside.move_up()
        if ctop.get_rect().centerx > ballx and ctop.get_rect().left >= 0:
            ctop.move_left()
            cbot.move_left()
        if ctop.get_rect().centerx < ballx and ctop.get_rect().right <= WINDOWWIDTH / 2:
            ctop.move_right()
            cbot.move_right()

        # draw screen
        surface.fill(BLACK)

        # draw scores
        # player score
        draw_text('Game Score: %s' % (player_score), default_font, surface, WINDOWWIDTH * 3/4 - 50, 50)
        draw_text('Match Score: %s' % (player_match), default_font, surface, WINDOWWIDTH * 3/4 - 50, 70)
        draw_text('Number of points needed: %s' % (points_needed), default_font, surface, WINDOWWIDTH * 3/4 - 50, 90)
        # computer score
        draw_text('Game Score: %s' % (computer_score), default_font, surface, WINDOWWIDTH / 4 - 50, 50)
        draw_text('Match Score: %s' % (computer_match), default_font, surface, WINDOWWIDTH / 4 - 50, 70)

        # draw objects onto surface
        # draw net
        # net has line length of 10 and a gap of 5
        starty = 0
        while starty <= WINDOWHEIGHT:
            pygame.draw.line(surface, GRAY, (WINDOWWIDTH/2, starty), (WINDOWWIDTH/2, starty + 10))
            starty += 15


        # draw vertical paddles
        for p in vpaddles:
            rect = pygame.draw.rect(surface, BLACK, p.get_rect())
            surface.blit(verticleimage, rect)

        # draw horizontal paddles
        for p in hpaddles:
            rect = pygame.draw.rect(surface, BLACK, p.get_rect())
            surface.blit(horizontalimage, rect)

        # draw ball
        ball = pygame.draw.circle(surface, WHITE, (int(ballx), int(bally)), RADIUS)

        # check if ball has collided with wall
        # calculate score
        # based on which side the ball is on when it hits a wall
        if bally - RADIUS <= 0 or bally + RADIUS >= WINDOWHEIGHT:
            if ballx < WINDOWWIDTH / 2:
                player_score += 1
                wingame.play()
                draw_text('Congratulations! You won the game.', default_font, surface, WINDOWWIDTH / 2 - 100,
                          WINDOWHEIGHT / 2 - 100)

            elif ballx > WINDOWWIDTH / 2:
                computer_score += 1
                losegame.play()
                draw_text('Sorry, computer won the game.', default_font, surface, WINDOWWIDTH / 2 - 100,
                          WINDOWHEIGHT / 2 - 100)

            # default is middle of screen
            ballx = WINDOWWIDTH / 2
            bally = WINDOWHEIGHT / 2

            # random velocity
            velx = random.randint(-5, 6)
            vely = random.randint(-5, 6)
            ball_speed = random.randint(1, 11)

        if ballx - RADIUS <= 0 or ballx + RADIUS >= WINDOWWIDTH:
            if ballx < WINDOWWIDTH / 2:
                player_score += 1
                wingame.play()
                draw_text('Congratulations! You won the game.', default_font, surface, WINDOWWIDTH / 2 - 100,
                          WINDOWHEIGHT / 2 - 100)

            elif ballx > WINDOWWIDTH / 2:
                computer_score += 1
                losegame.play()
                draw_text('Sorry, computer won the game.', default_font, surface, WINDOWWIDTH / 2 - 100,
                          WINDOWHEIGHT / 2 - 100)

            # default is middle of screen
            ballx = WINDOWWIDTH / 2
            bally = WINDOWHEIGHT / 2

            # random velocity
            velx = random.randint(-5, 6)
            vely = random.randint(-5, 6)
            ball_speed = random.randint(1, 11)

        # Check if the ball has collided with any horizontal paddles.
        for paddle in hpaddles[:]:
            if ball.colliderect(paddle.get_rect()):
                vely *= -1
                bounce.play()

        # check if ball collided with any vertical paddles
        for paddle in vpaddles[:]:
            if ball.colliderect(paddle.get_rect()):
                velx *= -1
                bounce.play()

        # move ball
        ballx += velx * ball_speed
        bally += vely * ball_speed

        # check for match points
        if player_score >= 11 and (player_score-computer_score) >= 2:
            player_score = 0
            computer_score = 0
            points_needed = 11
            player_match += 1
            winmatch.play()
        elif computer_score >= 11 and (computer_score-player_score) >= 2:
            player_score = 0
            computer_score = 0
            points_needed = 11
            computer_match += 1
            losematch.play()

        # check for Game Over
        if player_match >= 3:
            draw_text('Congratulations! You won the match!', default_font, surface, WINDOWWIDTH/2 - 100, WINDOWHEIGHT/2 - 100)
            gameover = True
        if computer_match >= 3:
            draw_text('Sorry! Computer won the match!', default_font, surface, WINDOWWIDTH/2 - 100, WINDOWHEIGHT/2 - 100)
            gameover = True

        # calculate points needed
        if computer_score <= 9:
            points_needed = 11 - player_score
        else:
            points_needed = computer_score + 2 - player_score


        pygame.display.update()
        clock.tick(40)

    draw_text('Do you want to play again? (y or n)', default_font, surface, WINDOWWIDTH/2 - 200, WINDOWHEIGHT/2)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_y:
                # restart
                # initialize all variables back to default

                cside = Paddle(rect=(0, (WINDOWHEIGHT - VPADDLEHEIGHT) / 2, VPADDLEWIDTH, VPADDLEHEIGHT), scale=SPEED)
                ctop = Paddle(rect=((WINDOWWIDTH / 4) - (HPADDLEWIDTH / 2), 0, HPADDLEWIDTH, HPADDLEHEIGHT),
                              scale=SPEED)
                cbot = Paddle(
                    rect=(
                    (WINDOWWIDTH / 4) - (HPADDLEWIDTH / 2), WINDOWHEIGHT - HPADDLEHEIGHT, HPADDLEWIDTH, HPADDLEHEIGHT),
                    scale=SPEED)
                pside = Paddle(
                    rect=(WINDOWWIDTH - VPADDLEWIDTH, (WINDOWHEIGHT - VPADDLEHEIGHT) / 2, VPADDLEWIDTH, VPADDLEHEIGHT),
                    scale=SPEED)
                ptop = Paddle(rect=((WINDOWWIDTH * 3 / 4) - (HPADDLEWIDTH / 2), 0, HPADDLEWIDTH, HPADDLEHEIGHT),
                              scale=SPEED)
                pbot = Paddle(rect=(
                    (WINDOWWIDTH * 3 / 4) - (HPADDLEWIDTH / 2), WINDOWHEIGHT - HPADDLEHEIGHT, HPADDLEWIDTH,
                    HPADDLEHEIGHT),
                    scale=SPEED)

                # default scores
                player_score = 0
                computer_score = 0
                player_match = 0
                computer_match = 0
                points_needed = 11

                # ball position
                # default is middle of screen
                ballx = WINDOWWIDTH / 2
                bally = WINDOWHEIGHT / 2

                # random velocity
                velx = random.randint(-5, 6)
                vely = random.randint(-5, 6)
                ball_speed = random.randint(1, 11)

                gameover = False

            if event.key == K_n:
                play_again = False

pygame.quit()
sys.exit()
