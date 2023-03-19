from pygame.locals import *

def keydown_handler(event, player, current_room, blocking_tiles):
    index = 0
    increment = 0 
    if event.key == K_w:
        index = 0
        increment = -1
    elif event.key == K_a:
        index = 1
        increment = -1
    elif event.key == K_s:
        index = 0
        increment = 1
    elif event.key == K_d:
        index = 1
        increment = 1

    new_player_row_col = player.row_col.copy() 
    new_player_row_col[index] += increment

    x = new_player_row_col[1]
    y = new_player_row_col[0]
    next_tile = current_room[y][x] 

    conditions = [
        not next_tile,
        next_tile not in blocking_tiles,
    ]

    if all(conditions):
        old_x = player.row_col[1]
        old_y = player.row_col[0]
        current_room[old_y][old_x] = ''

        player.row_col = new_player_row_col
        current_room[y][x] = player.symbol