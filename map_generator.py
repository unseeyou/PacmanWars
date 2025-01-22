import random
import copy
from constants import *
from collections import deque

# Function to generate a random shaped map
# (DO NOT CHANGE THIS, YOUR CHANGES WILL BE IGNORED IN THE COMPETITION)
def generate_random_shaped_map(length: int, breadth: int, probability: float) -> list:
    """
    Generate a map of given length and breadth. Give shape to the map by marking
    edge cells as out_of_bounds with given succeeding probability.
    :param length: Length of the map
    :param breadth: Breadth of the map
    :param probability: Probability of a cell being out_of_bounds subsequent to the previous cell.
    """
    if probability < 0 or probability > MAX_OUT_OF_BOUND_PROBABILITY:
        raise ValueError(f"Probability should be between 0 and {MAX_OUT_OF_BOUND_PROBABILITY}")
    if length < 1 or breadth < 1:
        raise ValueError("Length and breadth should be greater than 0.")
    if probability == 0:
        return [[WALKABLE_CELL for _ in range(breadth)] for _ in range(length)]
    
    map = []
    for i in range(length):
        row = []
        for j in range(breadth):
            # Mark 2 layer of edge cells as out_of_bounds
            if i in [0, 1] or j in [0, 1] or i in [length-1, length-2] or j in [breadth-1, breadth-2]:
                row.append(OUT_OF_BOUNDS_CELL)  
            else:
                row.append(WALKABLE_CELL)
        map.append(row)
    
    for i in range(2, length-2):
        for j in range(2, breadth-3):
            if random.random() > probability:   # Probability of a cell being out_of_bounds from left
                break
            map[i][j] = OUT_OF_BOUNDS_CELL

        for j in range(2, breadth-3):
            if map[i][breadth - j - 2] == OUT_OF_BOUNDS_CELL or random.random() > probability:   # Probability of a cell being out_of_bounds from right
                break
            map[i][breadth - j - 1] = OUT_OF_BOUNDS_CELL
    return map

# Function to check if the generated map is valid or not
# (DO NOT CHANGE THIS, YOUR CHANGES WILL BE IGNORED IN THE COMPETITION)
def check_if_map_is_valid(map: list) -> bool:
    """
    Check if all the green cells are one connected component to ensure map is valid.
    :param map: 2D list representing the game map
    """
    def bfs(start_i, start_j):
        queue = deque([(start_i, start_j)])
        while queue:
            i, j = queue.popleft()
            if i < 0 or i >= len(map) or j < 0 or j >= len(map[0]) or map_copy[i][j] != WALKABLE_CELL:
                continue
            map_copy[i][j] = '0'
            queue.append((i+1, j)) # Down
            queue.append((i-1, j)) # Up
            queue.append((i, j+1)) # Right
            queue.append((i, j-1)) # Left
    
    # Create a deep copy of the map to avoid modifying the original map
    map_copy = copy.deepcopy(map)
    
    # Find the first green cell and start bfs from there.
    for j in range(len(map_copy[0])):
        if map_copy[2][j] == WALKABLE_CELL:     # Start from 2nd row to avoid edge cells
            bfs(2, j)
            break
    
    # Check if all green cells are visited.
    for i in range(len(map_copy)):
        for j in range(len(map_copy[0])):
            if map_copy[i][j] == WALKABLE_CELL:
                return False
    return True
    
# Function to generate mountains on the map
# (DO NOT CHANGE THIS, YOUR CHANGES WILL BE IGNORED IN THE COMPETITION)
def generate_mountains(map: list, num_of_cells: int, min_mountain_size: int, max_mountain_size: int, mountain_length_probability: float):
    """
    Generate mountains on the map by selecting random cell and creating a cluster of
    mountain cells of random size around it.
    :param map: 2D list representing the game map
    :param num_of_cells: Number of mountain cells to be generated
    :param min_mountain_size: Minimum size of mountain cluster
    :param max_mountain_size: Maximum size of mountain cluster
    :param mountain_length_probability: Probability of a mountain cell being generated in a continuous row
    """
    if num_of_cells < 0:
        raise ValueError("Number of mountain cells should be greater than 0.")
    if min_mountain_size < 1 or max_mountain_size < 1:
        raise ValueError("Minimum and maximum mountain size should be greater than 0.")
    if min_mountain_size > max_mountain_size:
        raise ValueError("Minimum mountain size should be less than or equal to maximum mountain size.")
    if mountain_length_probability < 0 or mountain_length_probability > 1:
        raise ValueError("Mountain length probability should be between 0 and 1.")
    
    mountain_cells = 0
    while mountain_cells < num_of_cells:
        # Select random walkable cell to start mountain from.
        while True:
            i = random.randint(0, len(map)-1)
            j = random.randint(0, len(map[0])-1)
            if map[i][j] == WALKABLE_CELL:
                break

        max_size = min(random.randint(min_mountain_size, max_mountain_size), num_of_cells - mountain_cells)
        current_mountain_size = 0

        loopj = j
        direction = 0   # 0: Right, 1: Left, Generate mountain cells in both the directions
        
        def is_valid_index(i, j):
            return i >= 0 and i < len(map) and j >= 0 and j < len(map[0]) and map[i][j] == WALKABLE_CELL

        while current_mountain_size < max_size:
            if direction == 0:  # Right
                if is_valid_index(i, loopj) and map[i][loopj] == WALKABLE_CELL and random.random() < mountain_length_probability:
                    map[i][loopj] = MOUNTAIN_CELL
                    current_mountain_size += 1
                    loopj += 1
                else:
                    direction = 1   # Change direction to left
                    loopj = j-1
            else:   # Left
                if is_valid_index(i, loopj) and map[i][loopj] == WALKABLE_CELL and random.random() < mountain_length_probability:
                    map[i][loopj] = MOUNTAIN_CELL
                    current_mountain_size += 1
                    loopj -= 1
                else:
                    i = i+1
                    direction = 0   # Change direction to right
                    if not is_valid_index(i, j) or map[i][j] != WALKABLE_CELL:  # Check if next row is walkable
                        break
        
        mountain_cells += current_mountain_size

# Function to generate a valid map
# (DO NOT CHANGE THIS, YOUR CHANGES WILL BE IGNORED IN THE COMPETITION)
def generate_map(out_of_bounds_probability: float, mountain_probability: float, mountain_coverage: int):
    """
    Generate a valid map with out_of_bounds cells and mountains.
    :param out_of_bounds_probability: Probability of a cell being out_of_bounds
    :param mountain_probability: Probability of a cell being mountain
    :param mountain_coverage: Number of mountain cells to be generated
    """
    # Generate a random shaped valid map
    m = generate_random_shaped_map(ROWS, COLS, out_of_bounds_probability)
    while not check_if_map_is_valid(m):
        m = generate_random_shaped_map(ROWS, COLS, out_of_bounds_probability)
    
    # Generate mountains on the map and ensure map remains valid
    mm = copy.deepcopy(m)
    generate_mountains(mm, mountain_coverage, 10, 20, mountain_probability)
    while not check_if_map_is_valid(mm):
        mm = copy.deepcopy(m)
        generate_mountains(mm, mountain_coverage, 10, 20, mountain_probability)
    return mm