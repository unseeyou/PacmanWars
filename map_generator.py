import random
import copy
from constants import *
from collections import deque

def generate_random_shaped_map(length: int, breadth: int, probability: float):
    """
    Generate a map of given length and breadth. Give shape to the map by marking
    edge cells as out_of_bounds with given probability.
    """
    if probability < 0 or probability > 0.8:
        raise ValueError("Probability should be between 0 and 0.8.")
    if length < 1 or breadth < 1:
        raise ValueError("Length and breadth should be greater than 0.")
    if probability == 0:
        return [[WALKABLE_CELL for _ in range(breadth)] for _ in range(length)]
    if probability == 1:
        return [[OUT_OF_BOUNDS_CELL for _ in range(breadth)] for _ in range(length)]
    
    map = []
    for i in range(length):
        row = []
        for j in range(breadth):
            if i in [0, 1] or j in [0, 1] or i in [length-1, length-2] or j in [breadth-1, breadth-2]:
                row.append(OUT_OF_BOUNDS_CELL)  
            else:
                row.append(WALKABLE_CELL)
        map.append(row)
    
    for i in range(length):
        for j in range(breadth-1):
            if random.random() > probability:
                break
            map[i][j] = OUT_OF_BOUNDS_CELL

        for j in range(breadth-1):
            if random.random() > probability:
                break
            map[i][breadth - j - 1] = OUT_OF_BOUNDS_CELL

    return map

def check_if_map_is_valid(map: list) -> bool:
    """
    Check if all the green cells are one connected component to ensure map is valid.
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
        if map_copy[2][j] == WALKABLE_CELL:
            bfs(2, j)
            break
    
    # Check if all green cells are visited.
    for i in range(len(map_copy)):
        for j in range(len(map_copy[0])):
            if map_copy[i][j] == WALKABLE_CELL:
                return False
    return True
    
def generate_mountains(map: list, num_of_cells: int, min_mountain_size: int, max_mountain_size: int, mountain_length_probability: float):
    """
    Generate mountains on the map by selecting random cell and creating a cluster of
    mountain cells of random size around it. 
    """
    if num_of_cells < 0:
        raise ValueError("Number of mountain cells should be greater than 0.")
    if min_mountain_size < 1 or max_mountain_size < 1:
        raise ValueError("Minimum and maximum mountain size should be greater than 0.")
    if min_mountain_size > max_mountain_size:
        raise ValueError("Minimum mountain size should be less than or equal to maximum mountain size.")
    
    mountain_cells = 0
    while mountain_cells < num_of_cells:
        # Select random cell to start mountain from.
        while True:
            i = random.randint(0, len(map)-1)
            j = random.randint(0, len(map[0])-1)
            if map[i][j] == WALKABLE_CELL:
                break

        max_size = min(random.randint(min_mountain_size, max_mountain_size), num_of_cells - mountain_cells)
        count = 0

        loopj = j
        direction = 0
        
        def is_valid(i, j):
            return i >= 0 and i < len(map) and j >= 0 and j < len(map[0]) and map[i][j] == WALKABLE_CELL

        while count < max_size:
            if direction == 0:
                if is_valid(i, loopj) and map[i][loopj] == WALKABLE_CELL and random.random() < mountain_length_probability:
                    map[i][loopj] = MOUNTAIN_CELL
                    count += 1
                    loopj += 1
                else:
                    direction = 1
                    loopj = j-1
            else:
                if is_valid(i, loopj) and map[i][loopj] == WALKABLE_CELL and random.random() < mountain_length_probability:
                    map[i][loopj] = MOUNTAIN_CELL
                    count += 1
                    loopj -= 1
                else:
                    i = i+1
                    direction = 0
                    if not is_valid(i, j) or map[i][j] != WALKABLE_CELL:
                        break
        
        mountain_cells += count

def generate_map(shape_probability: float, mountain_probability: float, mountain_coverage: int):
    m = generate_random_shaped_map(ROWS, COLS, shape_probability)
    while not check_if_map_is_valid(m):
        m = generate_random_shaped_map(ROWS, COLS, shape_probability)
    mm = copy.deepcopy(m)
    generate_mountains(mm, mountain_coverage, 10, 20, mountain_probability)
    while not check_if_map_is_valid(mm):
        mm = copy.deepcopy(m)
        generate_mountains(mm, mountain_coverage, 10, 20, mountain_probability)
    return mm