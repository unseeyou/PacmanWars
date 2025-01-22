import random
from constants import *

# Function to generate food items on the map
# (DO NOT CHANGE THIS, YOUR CHANGES WILL BE IGNORED IN THE COMPETITION)
def generate_food(map: list, quantity: int):
    """
    Generate new food items on the map after all the bots have moved.
    :param map: 2D list representing the game map
    :param quantity: Number of food items to generate
    """
    length, breadth = len(map), len(map[0])
    if quantity < 0:
        raise ValueError("Quantity should be greater than 0.")
    
    num_of_walkable_cells = 0
    for i in range(length):
        for j in range(breadth):
            if map[i][j] == WALKABLE_CELL:
                num_of_walkable_cells += 1

    quantity = min(quantity, num_of_walkable_cells//2)  # Generate food items on maximum half of the walkable cells

    for _ in range(quantity):
        while True:
            x, y = random.randint(0, length-1), random.randint(0, breadth-1)
            if map[x][y] == WALKABLE_CELL:  # Generate food item on a walkable cell
                map[x][y] = FOOD_CELL
                break