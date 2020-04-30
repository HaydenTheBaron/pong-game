# main.py

"""This file contains the starting point for this pong game,
as well as some helper methods."""

import pygame, sys, random
from pygame.locals import *  # TODO: do I need this extra import?
import globals
import events
from paddle import _Paddle
from playerpaddle import PlayerPaddle
from aipaddle import AIPaddle
from ball import Ball





def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)



def main_menu(screen, font, clock, score_font, victory_font):
    """Launches the main menu."""

    while True:

        screen.fill((0,0,0))
        draw_text('main menu', font, (255, 255, 255), screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(50, 100, 200, 50)
        button_2 = pygame.Rect(50, 200, 200, 50)

        if button_1.collidepoint((mx, my)):
            if globals.click_flag:
                game(screen, clock, score_font, victory_font)
        if button_2.collidepoint((mx, my)):
            if globals.click_flag:
                options(screen, clock, font)
        pygame.draw.rect(screen, (255, 0, 0), button_1)
        pygame.draw.rect(screen, (255, 0, 0), button_2)

        globals.click_flag = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    globals.click_flag = True

        pygame.display.update()
        clock.tick(60)


def game(screen, clock, score_font, victory_font):
    """Launches the game."""

    # ==========================================================
    # Init game objects
    # ==========================================================

    ball = Ball(30, pygame.Color('yellow'),
                globals.DEF_BALL_SPEED * random.choice((1, -1)),
                globals.DEF_BALL_SPEED * random.choice((1, -1)))
    player1 = PlayerPaddle(globals.P1_COLOR_TUPLE, 'right')

    # Create 2nd player paddle on pvp mode, AI paddle on single player mode
    if globals.game_mode == 'pvp':
        player2 = PlayerPaddle(globals.P2_COLOR_TUPLE, 'left')
    else:  # if globals.game_mode == 'single_player'
        player2 = AIPaddle(globals.P2_COLOR_TUPLE, 'left', ball)


    # ==========================================================
    # Init game flags
    # ==========================================================

    was_point_scored = False


    # ==========================================================
    # Init score
    # ==========================================================

    player1_score = 0
    player2_score = 0
    player1_score_surface = score_font.render(str(player1_score),
                                           True, player1.color_tuple)
    player2_score_surface = score_font.render(str(player2_score),
                                        True, player2.color_tuple)
    victory_message_surface = None


    # ==========================================================
    # Game loop
    # ==========================================================

    running = True
    while running:

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Event processing loop
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        for event in pygame.event.get():

            ##################################
            # DEBUG OUTPUT
            #print('event: ', event)
            #print('type: ', event.type)
            ##################################

            # Handle victory events
            # ---------------------------------------------
            if player1_score >= globals.POINTS_TO_WIN:
                pygame.event.post(events.right_side_wins)
            elif player2_score >= globals.POINTS_TO_WIN:
                pygame.event.post(events.left_side_wins)


            # Handle quit event
            # ---------------------------------------------
            if event.type == pygame.QUIT:  # Exit the game
                pygame.quit()
                sys.exit()


            # Handle player1 input events
            # ---------------------------------------------
            if event.type == pygame.KEYDOWN:  # Keydown controls
                if event.key == pygame.K_DOWN:
                    player1.y_speed += globals.DEF_PADDLE_SPEED
                if event.key == pygame.K_UP:
                    player1.y_speed -= globals.DEF_PADDLE_SPEED
            if event.type == pygame.KEYUP:    # Keyup controls
                if event.key == pygame.K_DOWN:
                    player1.y_speed -= globals.DEF_PADDLE_SPEED
                if event.key == pygame.K_UP:
                    player1.y_speed += globals.DEF_PADDLE_SPEED


            # Handle player2 input events (if in a multiplayer mode)
            # ---------------------------------------------

            if globals.game_mode == 'pvp':
                if event.type == pygame.KEYDOWN:  # Keydown controls
                    if event.key == pygame.K_s:
                        player2.y_speed += globals.DEF_PADDLE_SPEED
                    if event.key == pygame.K_w:
                        player2.y_speed -= globals.DEF_PADDLE_SPEED
                if event.type == pygame.KEYUP:    # Keyup controls
                    if event.key == pygame.K_s:
                        player2.y_speed -= globals.DEF_PADDLE_SPEED
                    if event.key == pygame.K_w:
                        player2.y_speed += globals.DEF_PADDLE_SPEED

            # Handle goal score events
            # ---------------------------------------------

            if event.type == events.LEFT_GOAL_SCORED_IN_TYPE or \
                    event.type == events.RIGHT_GOAL_SCORED_IN_TYPE:
                player1.reset_position('right')
                player2.reset_position('left')
                ball.restart()
                was_point_scored = True
                if event.type == events.LEFT_GOAL_SCORED_IN_TYPE:
                    print('LEFT GOAL SCORED IN')
                    player1_score += 1
                    victory_message_surface = victory_font.render('right\'s point!',
                                                                True,
                                                                player1.color_tuple)
                elif event.type == events.RIGHT_GOAL_SCORED_IN_TYPE:
                    print('RIGHT GOAL SCORED IN')
                    player2_score += 1
                    victory_message_surface = victory_font.render('left\'s point!',
                                                                True,
                                                                player2.color_tuple)
            else:
                victory_message_surface = None


            if event.type == events.LEFT_SIDE_WINS_TYPE:
                print('LEFT SIDE WINS')
                victory_message_surface = victory_font.render('LEFT SIDE WINS!',
                                                       True,
                                                       player2.color_tuple)
                running = False  # The game loop will not run again
            if event.type == events.RIGHT_SIDE_WINS_TYPE:
                print('RIGHT SIDE WINS')
                victory_message_surface = victory_font.render('RIGHT SIDE WINS!',
                                                       True,
                                                       player1.color_tuple)
                running = False  # The game loop will not run again



        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Update game models
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # Shift game object locations
        # ---------------------------------------------
        ball.move_to_next_frame(player1, player2)
        player1.move_to_next_frame()
        player2.move_to_next_frame()


        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Draw
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # Draw game objects
        # ---------------------------------------------

        screen.fill(globals.BG_COLOR)
        pygame.draw.rect(screen,
                         player1.color_tuple,
                         player1)
        pygame.draw.rect(screen,
                         player2.color_tuple,
                         player2)
        pygame.draw.aaline(screen,
                           globals.MIDLINE_COLOR_TUPLE,
                        (globals.SCREEN_WIDTH/2, 0),
                        (globals.SCREEN_WIDTH/2, globals.SCREEN_HEIGHT))
        pygame.draw.ellipse(screen,
                            ball.color_tuple,
                            ball.rect)


        # Draw score
        # ---------------------------------------------

        player1_score_surface = score_font.render(str(player1_score),
                                           True, player1.color_tuple)
        player2_score_surface = score_font.render(str(player2_score),
                                        True, player2.color_tuple)
        screen.blit(player1_score_surface, (globals.SCREEN_WIDTH -80, 20))
        screen.blit(player2_score_surface, (60, 20))

        if victory_message_surface is not None:
            screen.blit(victory_message_surface,
                                (globals.SCREEN_WIDTH/2 - 400,
                                 globals.SCREEN_HEIGHT/2))

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Refresh display
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # Update the window
        pygame.display.flip()
        clock.tick(globals.FRAME_RATE)


        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Post-refresh
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # Pause if point was scored
        if was_point_scored:
            pygame.time.delay(globals.PAUSE_ON_GOAL_MS)  # Pause game for 1000 ms
            was_point_scored = False


def options(screen, clock, font):
    running = True
    while running:
        screen.fill((0,0,0))

        draw_text('options', font, (255, 255, 255), screen, 20, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        clock.tick(60)



def main():
    """The starting point for this program."""

    # ==========================================================
    # General setup
    # ==========================================================

    globals.init()
    events.init()
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption('pong-game')

    def_font = pygame.font.SysFont(None, 20)
    score_font = pygame.font.SysFont('Helvetica',  # Init text drawer
                                   48, bold=True, italic=False)
    victory_font = pygame.font.SysFont('Helvetica',  # Init text drawer
                                       100, bold=True, italic=True)
    screen = pygame.display.set_mode((globals.SCREEN_WIDTH, globals.SCREEN_HEIGHT))

    # ==========================================================
    # Run game
    # ==========================================================

    main_menu(screen, def_font, clock, score_font, victory_font)

    # ==========================================================
    # Exiting
    # ==========================================================

    pygame.time.delay(globals.PAUSE_ON_WIN_MS)
    pygame.quit()



if __name__ == '__main__':
    main()
