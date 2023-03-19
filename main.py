import pygame, sys
from pygame.locals import *

from constants import *
from helpers import *
from event_handlers import *

#Set up pygame
pygame.init()

#Set up the window
WIDTH = 800
HEIGHT = 600
TILE_DIM = 16
window_surface = pygame.display.set_mode((WIDTH, HEIGHT), 0 , 32)
pygame.display.set_caption('builder-game')

#Set up fonts
main_font = pygame.font.Font('./Minecraft.ttf', TILE_DIM)

target_coords = (0,0)

current_room_width = 50
current_room_height = 37
current_room = [['' for x in range(current_room_width)] for y in range(current_room_height)]

initial_player_row = current_room_height//2
initial_player_col = current_room_width//2

current_room[initial_player_row][initial_player_col] = player.symbol
player.row_col = [initial_player_row, initial_player_col]

blocking_tiles = ['#']
mouse_down = False

#Run the game loop
while True:
    # clear window
    window_surface.fill(colors.bg_color)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # get mouse move
        elif event.type == MOUSEMOTION:
            target_coords = tuple_op(event.pos, lambda x: int(x/TILE_DIM)*TILE_DIM)

        # get mouse click
        elif event.type == MOUSEBUTTONDOWN:
            mouse_down = True

        # get mouse release
        elif event.type == MOUSEBUTTONUP:
            mouse_down = False

        # get key press
        elif event.type == KEYDOWN:
            keydown_handler(event, player, current_room, blocking_tiles)


    # process state after events handled
    if mouse_down:
        t = tuple_op(target_coords, lambda x: int(x/TILE_DIM))
        row = t[1] 
        col = t[0] 
        player_x = player.row_col[1]
        player_y = player.row_col[0]
        player.action = 'build'

        # handle user interaction with space
        conditions = [
            # check if within bounds
            row < current_room_height,
            row >= 0,
            col < current_room_width,
            col >= 0,
            # check if space is empty
            not current_room[row][col],
            # check if within player range
            abs(player_x - col) <= player.reach,
            abs(player_y - row) <= player.reach,
        ]
        if all(conditions) and player.action:
            if player.action == 'build':
                current_room[row][col] = '#'

    # draw blocks
    for row_index, row in enumerate(current_room):
        for tile_index, tile in enumerate(row):
            if tile:
                # draw text
                tile_color = colors.brown
                if tile == player.symbol:
                 tile_color = player.color

                text = main_font.render(tile, True, tile_color, colors.bg_color)
                text_rect = text.get_rect()
                text_rect.centerx = tile_index*TILE_DIM + TILE_DIM/2
                text_rect.centery = row_index*TILE_DIM + TILE_DIM/2
                window_surface.blit(text, text_rect)


    # draw target
    x_coord = target_coords[0]
    y_coord = target_coords[1]

    print(target_coords)

    target_coords_normalized = tuple_op(target_coords, lambda x: int(x/TILE_DIM))
    x_coord_normalized = target_coords_normalized[0]
    y_coord_normalized = target_coords_normalized[1]

    target_color = colors.white 
    if abs(player.row_col[1] - x_coord_normalized) <= player.reach and abs(player.row_col[0] - y_coord_normalized) <= player.reach:
        target_color = colors.green

    pygame.draw.rect(window_surface, target_color, (x_coord, y_coord, TILE_DIM, TILE_DIM), 1)

    pygame.display.update()