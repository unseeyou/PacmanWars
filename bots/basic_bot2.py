from .bot import Bot
from constants import *

class BasicBot2(Bot):
    def __init__(self, id: int, start_x: int, start_y: int, minimap: list, map_length: int, map_breadth: int):
        super().__init__(id, start_x, start_y, minimap, map_length, map_breadth)

    def move(self, current_x:int, current_y:int, minimap:list, bot_food:dict) -> int:
        self.update_state(current_x, current_y, minimap, bot_food)
        if self.map[current_x][current_y+1] not in [OUT_OF_BOUNDS_CELL, MOUNTAIN_CELL]:
            return MOVE_RIGHT
        elif self.map[current_x+1][current_y] not in [OUT_OF_BOUNDS_CELL, MOUNTAIN_CELL]:
            return MOVE_DOWN
        elif self.map[current_x][current_y-1] not in [OUT_OF_BOUNDS_CELL, MOUNTAIN_CELL]:
            return MOVE_LEFT
        elif self.map[current_x-1][current_y] not in [OUT_OF_BOUNDS_CELL, MOUNTAIN_CELL]:
            return MOVE_UP
        else:
            return MOVE_HALT