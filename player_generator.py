import random
from constants import *

def generate_player(map: list, num_of_players: int):
    """
    Generate a snapshot of players on the map.
    """
    if num_of_players < 0:
        raise ValueError("Number of players should be greater than 0.")

    players = dict()
    for idx in range(0, num_of_players):
        while True:
            i = random.randint(0, len(map)-1)
            j = random.randint(0, len(map[0])-1)
            if map[i][j] == WALKABLE_CELL:
                map[i][j] = str(idx + 1)
                players[idx+1] = [i, j]
                break
    
    return players