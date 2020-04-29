#
# globals.py
#

import pygame


def init():

    # Declare constants
    global BG_COLOR
    global MIDLINE_COLOR_TUPLE
    global SCREEN_WIDTH
    global SCREEN_HEIGHT
    global FRAME_RATE
    global screen
    global POINTS_TO_WIN

    # Declare global game objects
    global ball
    global player
    global bot

    # Initialize constants
    BG_COLOR = pygame.Color('black')
    MIDLINE_COLOR_TUPLE = (255, 255, 255)
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 960
    FRAME_RATE = 60
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    POINTS_TO_WIN = 3
