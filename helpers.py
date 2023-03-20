def tuple_op(t, func):
    return tuple(map(func, t))

def check_bounds(room, row, col):
    return row < room.height and row >= 0 and col < room.width and col >= 0