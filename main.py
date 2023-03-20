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

initial_player_row = current_room.height//2
initial_player_col = current_room.width//2

current_room.set(initial_player_row, initial_player_col, player.symbol)
player.row_col = [initial_player_row, initial_player_col]

blocking_tiles = ['#']
mouse_down = False
prevent_mouse_down = False

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
            # get left click
            if event.button == 1:
                player.action = 'build'
            # get right click
            elif event.button == 3:
                player.action = 'break'

        # get mouse release
        elif event.type == MOUSEBUTTONUP:
            mouse_down = False
            prevent_mouse_down = False
            player.action = None

        # get key press
        elif event.type == KEYDOWN:
            keydown_handler(event, player, current_room, blocking_tiles)


    # process state after events handled
    if mouse_down and not prevent_mouse_down:
        t = tuple_op(target_coords, lambda x: int(x/TILE_DIM))
        row = t[1] 
        col = t[0] 
        player_x = player.row_col[1]
        player_y = player.row_col[0]

        # handle user interaction with space
        conditions = [
            # check if within bounds
            row < current_room.height,
            row >= 0,
            col < current_room.width,
            col >= 0,
            # check if within player range
            abs(player_x - col) <= player.reach,
            abs(player_y - row) <= player.reach,
        ]
        if all(conditions) and player.action:
            target_tile = current_room.get(row, col)
            if player.action == 'build' and target_tile == '':
                current_room.set(row, col, '#')
                player_event_log.add('built wooden fence at ' + str((col, row)))
            elif player.action == 'break' and target_tile and target_tile != '@':
                current_room.set(row, col, '')
                player_event_log.add('broke wooden fence at ' + str((col, row)))
        else:
            player_event_log.add('out of range at ' + str((col, row)))
            prevent_mouse_down = True 

    # draw blocks
    for row_index, row in enumerate(current_room.matrix):
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

    target_coords_normalized = tuple_op(target_coords, lambda x: int(x/TILE_DIM))
    x_coord_normalized = target_coords_normalized[0]
    y_coord_normalized = target_coords_normalized[1]

    # for describing tile to player
    looking_at_description = ''

    # check if target in bounds
    if check_bounds(current_room, y_coord_normalized, y_coord_normalized):
        print(target_coords, target_coords_normalized)

        # set tile description
        looking_at_tile = current_room.get(y_coord_normalized, x_coord_normalized)
        looking_at_description = descriptions.get(looking_at_tile)

        target_color = colors.white 
        if abs(player.row_col[1] - x_coord_normalized) <= player.reach and abs(player.row_col[0] - y_coord_normalized) <= player.reach:
            target_color = colors.green

        pygame.draw.rect(window_surface, target_color, (x_coord, y_coord, TILE_DIM, TILE_DIM), 1)

    # draw text area
    text_area = pygame.Rect(0, current_room.height * TILE_DIM, WIDTH, TILE_DIM * 11)
    pygame.draw.rect(window_surface, colors.black, text_area)

    # draw text to text area
    if looking_at_description:
        message = 'Looking at ' + looking_at_description + ' at ' + str(( x_coord_normalized, y_coord_normalized))
        text = main_font.render(message, True, colors.white, colors.black)
        text_rect = text.get_rect()
        # set coordinates to top left of text area
        text_rect.topleft = (0, current_room.height * TILE_DIM)
        window_surface.blit(text, text_rect)

    # render event log
    for i, event in enumerate(player_event_log.log):
        text = main_font.render(event, True, colors.white, colors.black)
        text_rect = text.get_rect()
        text_rect.topleft = (0, current_room.height * TILE_DIM + TILE_DIM * (i + 1))
        window_surface.blit(text, text_rect)


    pygame.display.update()