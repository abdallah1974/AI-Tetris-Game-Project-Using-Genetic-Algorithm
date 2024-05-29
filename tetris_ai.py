import random, time, pygame, sys
from pygame.locals import *
import tetris_base as game

size   = [640, 480]
screen = pygame.display.set_mode((size[0], size[1]))
NUM_ITER        = 1000

def run_game(chromosome, speed, max_score = 20000, no_show = False):

    game.FPS = int(speed)
    game.main()

    board            = game.get_blank_board()
    last_fall_time   = time.time()
    score            = 0
    level, fall_freq = game.calc_level_and_fall_freq(score)
    falling_piece    = game.get_new_piece()
    next_piece       = game.get_new_piece()

    # Calculate best move
    chromosome.calc_best_move(board, falling_piece)

    num_used_pieces = 0
    removed_lines   = [0,0,0,0]

    alive = True
    win   = False

    # Game loop
    while alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print ("Game exited by user")
                exit()

        if falling_piece == None:

            falling_piece = next_piece
            next_piece    = game.get_new_piece()

            chromosome.calc_best_move(board, falling_piece, no_show)

            
            num_used_pieces +=1
            score           += 1

            # if num_used_pieces > NUM_ITER:
            #     alive = False

            last_fall_time = time.time()

            if (not game.is_valid_position(board, falling_piece)):
               
                alive = False

        if no_show or time.time() - last_fall_time > fall_freq:
            if (not game.is_valid_position(board, falling_piece, adj_Y=1)):
               
                game.add_to_board(board, falling_piece)

                
                num_removed_lines = game.remove_complete_lines(board)
                if(num_removed_lines == 1):
                    score += 40
                    removed_lines[0] += 1
                elif (num_removed_lines == 2):
                    score += 120
                    removed_lines[1] += 1
                elif (num_removed_lines == 3):
                    score += 300
                    removed_lines[2] += 1
                elif (num_removed_lines == 4):
                    score += 1200
                    removed_lines[3] += 1

                falling_piece = None
            else:
                falling_piece['y'] += 1
                last_fall_time = time.time()

        if (not no_show):
            draw_game_on_screen(board, score, level, next_piece, falling_piece,chromosome)


        if (score > max_score):
            win   = True

    game_state = [num_used_pieces, removed_lines, score, win]

    return game_state

def draw_game_on_screen(board, score, level, next_piece, falling_piece, chromosome):
    """Draw game on the screen"""

    game.DISPLAYSURF.fill(game.BGCOLOR)
    game.draw_board(board)
    game.draw_status(score, level)
    game.draw_next_piece(next_piece)

    if falling_piece != None:
        game.draw_piece(falling_piece)

    pygame.display.update()
    game.FPSCLOCK.tick(game.FPS)
