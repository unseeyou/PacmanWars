import random
from .bot import Bot

class BasicBot2(Bot):
    def __init__(self, id: int, start_x: int, start_y: int, minimap: list, map_length: int, map_breadth: int):
        super().__init__(id, start_x, start_y, minimap, map_length, map_breadth)

    def move(self, current_x:int, current_y:int, minimap:list) -> int:
        self.minimap = minimap
        self.update_map_from_minimap()

        direction = random.randint(0, 4)
        self.x = current_x
        self.y = current_y
        return direction