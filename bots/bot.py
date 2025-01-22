from abc import ABC, abstractmethod
from constants import *

# Bot class that needs to be inherited by the bot implementation
# (DO NOT CHANGE THIS, YOUR CHANGES WILL BE IGNORED IN THE COMPETITION)
class Bot(ABC):
    def __init__(self, id: int, start_x: int, start_y: int, minimap: list, map_length: int, map_breadth: int):
        """
        Initialize the bot with its ID, starting x and y coordinates, initial minimap and map dimensions
        :param id: Bot ID
        :param start_x: Starting x coordinate
        :param start_y: Starting y coordinate
        :param minimap: Initial minimap
        :param map_length: Length of the overall map
        :param map_breadth: Breadth of the overall map
        """
        super().__init__()
        self.id = id            # Bot ID
        self.x = start_x        # Bot x coordinate
        self.y = start_y        # Bot y coordinate
        self.food = 1           # Bot food count
        self.minimap = minimap  # Bot minimap

        # Initally bot doesnt know the map, so think that entire map is unknown
        self.map = [[UNKNOWN_CELL for _ in range(map_breadth)] for _ in range(map_length)]
        self.update_map_from_minimap()

    def update_map_from_minimap(self):
        """
        Update the bot's map from the minimap
        """
        half_size = len(self.minimap) // 2
        for i in range(len(self.minimap)):
            for j in range(len(self.minimap[0])):
                map_x = self.x - half_size + i
                map_y = self.y - half_size + j
                if 0 <= map_x < len(self.map) and 0 <= map_y < len(self.map[0]):
                    self.map[map_x][map_y] = self.minimap[i][j]

    def update_state(self, current_x: int, current_y: int, minimap: list):
        self.x = current_x
        self.y = current_y
        self.minimap = minimap
        self.update_map_from_minimap()

    @abstractmethod
    def move(self, current_x: int, current_y: int, minimap: list) -> int:
        """
        Move the bot based on the current minimap
        :param current_x: Current x coordinate of the bot
        :param current_y: Current y coordinate of the bot
        :param minimap: 5x5 minimap of the bot
        :return: direction to move (MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT, MOVE_HALT)
        """
        raise NotImplementedError("You need to implement the move method in your bot class")
        