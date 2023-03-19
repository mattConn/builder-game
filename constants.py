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