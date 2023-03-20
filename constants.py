from helpers import *

# colors
class Colors:
    black = (0,0,0)
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)
    white = (255,255,255)
    yellow = (255,255,0)
    brown = (139,69,19)
    dark_brown = (101,67,33)
    grey = (128,128,128)
    bg_color = dark_brown 

colors = Colors()

# player
class Player:
    reach = 5
    moving = False
    row_col = [0,0]
    symbol = '@'
    color = colors.yellow
    action = None

player = Player()

class Room:
    def __init__(self, width = 0, height = 0):
        self.width = width 
        self.height = height 
        self.matrix = [['' for x in range(width)] for y in range(height)]

    def set(self, row, col, value):
        if not check_bounds(self, row, col):
            return False
        self.matrix[row][col] = value
        return True

    def get(self, row, col):
        if not check_bounds(self, row, col):
            return None 
        return self.matrix[row][col]

# 27 height leaves room for text
current_room = Room(50, 27)