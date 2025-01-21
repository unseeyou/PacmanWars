import random

class Bot:
    def __init__(self, player: int, x: int, y: int, minimap: list):
        self.player = player
        self.x = x
        self.y = y
        self.food = 1
        self.minimap = minimap

    def move(self, minimap):
        self.minimap = minimap
        direction = random.randint(0, 3)
        if direction == 0:  # up
            self.x -= 1
        elif direction == 1: # down
            self.x += 1
        elif direction == 2: # left
            self.y -= 1
        else: # right
            self.y += 1
        return direction