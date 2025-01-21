import random
from constants import *

def generate_food(map: list, quantity: int):
    """
    Generate a snapshot of food items on the map.
    """
    length, breadth = len(map), len(map[0])
    if quantity < 0:
        raise ValueError("Quantity should be greater than 0.")
    
    for _ in range(quantity):
        while True:
            x, y = random.randint(0, length-1), random.randint(0, breadth-1)
            if map[x][y] == WALKABLE_CELL:
                map[x][y] = FOOD_CELL
                break