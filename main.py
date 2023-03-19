import pygame, sys
from pygame.locals import *

#Set up pygame
pygame.init()

#Set up the window
WIDTH = 800
HEIGHT = 600
TILE_DIM = 16
windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0 , 32)
pygame.display.set_caption('Hello World')

#Set up the colors
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
YELLOW = (255,255,0)

#Set up fonts
basicFont = pygame.font.Font('./Minecraft.ttf', TILE_DIM)

target_pos = (0,0)
player_row_col = [0,0]

current_room_width = 50
current_room_height = 37
current_room = [['' for x in range(50)] for y in range(37)]
mouse_down = False
player_moving = False 

def tuple_op(t, func):
    return tuple(map(func, t))

#Run the game loop
while True:
    # clear window
    windowSurface.fill(BLACK)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # get mouse move
        if event.type == MOUSEMOTION:
            target_pos = tuple_op(event.pos, lambda x: int(x/TILE_DIM)*TILE_DIM)

        # get mouse click
        if event.type == MOUSEBUTTONDOWN:
            mouse_down = True

        # get mouse release
        if event.type == MOUSEBUTTONUP:
            mouse_down = False

        # get key press
        if event.type == KEYDOWN:
            index = 0
            increment = 0 
            if event.key == K_w:
                index = 0
                increment = -1
            if event.key == K_a:
                index = 1
                increment = -1
            if event.key == K_s:
                index = 0
                increment = 1
            if event.key == K_d:
                index = 1
                increment = 1

            new_player_row_col = player_row_col.copy() 
            new_player_row_col[index] += increment

            x = new_player_row_col[1]
            y = new_player_row_col[0]
            if not current_room[y][x]:
                old_x = player_row_col[1]
                old_y = player_row_col[0]
                current_room[old_y][old_x] = ''

                player_row_col = new_player_row_col
                current_room[y][x] = '@'


    if mouse_down:
        t = tuple_op(target_pos, lambda x: int(x/TILE_DIM))
        row = t[1] 
        col = t[0] 
        if row < current_room_height and row >= 0 and col < current_room_width and col >= 0:
            print('player_row_col', player_row_col)
            # if row != player_row_col[1] and col != player_row_col[0]:
            print("row: " + str(row) + " col: " + str(col))
            if not current_room[row][col]:
                current_room[row][col] = '#'

    # draw blocks
    for row_index, row in enumerate(current_room):
        for tile_index, tile in enumerate(row):
            if tile:
                # draw text
                text = basicFont.render(tile, True, WHITE, BLACK)
                textRect = text.get_rect()
                textRect.centerx = tile_index*TILE_DIM + TILE_DIM/2
                textRect.centery = row_index*TILE_DIM + TILE_DIM/2
                windowSurface.blit(text, textRect)

    # draw player
    text = basicFont.render('@', True, YELLOW, BLACK)
    textRect = text.get_rect()
    textRect.centerx = player_row_col[1]*TILE_DIM + TILE_DIM/2
    textRect.centery = player_row_col[0]*TILE_DIM + TILE_DIM/2
    windowSurface.blit(text, textRect)



    # draw target
    x_coord = target_pos[0]
    y_coord = target_pos[1]
    pygame.draw.rect(windowSurface, RED, (x_coord, y_coord, TILE_DIM, TILE_DIM), 1)

    pygame.display.update()