from .bot import Bot
from constants import *
import random

class BasicBot3(Bot):
    def __init__(self, id: int, start_x: int, start_y: int, minimap: list, map_length: int, map_breadth: int):
        super().__init__(id, start_x, start_y, minimap, map_length, map_breadth)

    def find_food(self):
        food_x, food_y = None, None
        for i in range(self.x-2, self.x+3):
            for j in range(self.y-2, self.y+3):
                if self.map[i][j] == FOOD_CELL:
                    food_x, food_y = i, j
                    break
        return food_x, food_y

    def move(self, current_x:int, current_y:int, minimap:list, bot_food:dict) -> int:
        self.update_state(current_x, current_y, minimap, bot_food)
        
        food_x, food_y = self.find_food()
        if food_x == None:
            return random.randint(0, 4)
        if food_x < self.x and self.map[self.x-1][self.y] in [FOOD_CELL, WALKABLE_CELL]:
            return MOVE_UP
        elif food_x > self.x and self.map[self.x+1][self.y] in [FOOD_CELL, WALKABLE_CELL]:
            return MOVE_DOWN
        elif food_y < self.y and self.map[self.x][self.y-1] in [FOOD_CELL, WALKABLE_CELL]:
            return MOVE_LEFT
        else:
            return MOVE_RIGHT