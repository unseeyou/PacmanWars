import os
import importlib
import random
from constants import *
from bots.bot import Bot
from typing import Dict

# Get the 5x5 minimap of the player
# (DO NOT CHANGE THIS, YOUR CHANGES WILL BE IGNORED IN THE COMPETITION)
def get_minimap(map, x, y):
    minimap = [row[y - 2: y+3] for row in map[x - 2: x+3]]
    return minimap

# Get the number of bots in the bots folder
# (DO NOT CHANGE THIS, YOUR CHANGES WILL BE IGNORED IN THE COMPETITION)
def get_number_of_bots():
    for filename in os.listdir('bots'):
        if filename.endswith('.py') and filename != 'bot.py':
            if filename.endswith('.py') and filename != 'bot.py':
                module_name = f'bots.{filename[:-3]}'
                _ = importlib.import_module(module_name)
    
    return len(Bot.__subclasses__())

# Load the all bots from the bot folder
# (DO NOT CHANGE THIS, YOUR CHANGES WILL BE IGNORED IN THE COMPETITION)
def load_bots(bot_positions: dict, map: list):
    bot_modules = Bot.__subclasses__()
    bot_names = {}
    bots = {}
    for ind, (x, y) in bot_positions.items():
        bot_instance = bot_modules[ind-1](ind, x, y, get_minimap(map, x, y), len(map), len(map[0]))
        bot_names[ind] = bot_instance.__class__.__name__
        bots[ind] = bot_instance
    return bots, bot_names

# Generate bot positions on the map
# (DO NOT CHANGE THIS, YOUR CHANGES WILL BE IGNORED IN THE COMPETITION)
def generate_bot_positions(map: list, num_of_bots: int) -> dict:
    """
    Generate bot positions on the map.
    :param map: 2D list representing the game map
    :param num_of_players: Number of bot positions to generate
    """
    if num_of_bots < 0:
        raise ValueError("Number of players should be greater than 0.")

    bot_positions = dict()    # Dictionary to store bot positions
    for idx in range(0, num_of_bots):
        while True:
            i = random.randint(0, len(map)-1)
            j = random.randint(0, len(map[0])-1)
            if map[i][j] == WALKABLE_CELL:  # Generate player on a walkable cell
                map[i][j] = str(idx + 1)    # Update the map with player number
                bot_positions[idx+1] = [i, j]     # Store player position
                break
    
    return bot_positions

# Execute bot code to find the next move
# (DO NOT CHANGE THIS, YOUR CHANGES WILL BE IGNORED IN THE COMPETITION)
def calculate_bot_directions(map: list, bots: Dict[int, Bot], bot_positions: dict, bot_ids: dict, bot_food: dict) -> dict:
    """
    Calculate the next move for each bot
    :param map: 2D list representing the game map
    :param bots: Dictionary containing bot objects
    :param bot_positions: Dictionary containing bot positions
    :param bot_ids: Dictionary containing bot ids
    :param bot_food: Dictionary containing { bot_id -> food count } mapping
    """
    bot_directions = {}
    for id, bot in bots.items():
        if bot_ids[id] == BOT_ALIVE:
            try:
                bot_directions[id] = bot.move(
                    current_x=bot_positions[id][0],
                    current_y=bot_positions[id][1],
                    minimap=get_minimap(map, bot_positions[id][0], bot_positions[id][1]),
                    bot_food=bot_food)
            except Exception:
                bot_directions[id] = MOVE_HALT
    return bot_directions

# Calculate final bot positions based on the directions bots are moving
# (DO NOT CHANGE THIS, YOUR CHANGES WILL BE IGNORED IN THE COMPETITION)
def calculate_final_bot_positions(map: list, bot_ids: dict, bot_current_positions: dict, bot_directions: dict):
    """
    Calculate the final positions of the bots based on the directions they are moving
    :param map: The 2D map of the game
    :param bot_ids: Dictionary containing the IDs of the bots
    :param bot_current_positions: Dictionary containing the current positions of the bots
    :param bot_directions: Dictionary containing the directions in which the bots are moving
    """
    bot_final_positions = dict()
    for id in bot_ids.keys():
        if bot_ids[id] == BOT_ALIVE:
            current_x, current_y = bot_current_positions[id]
            direction = bot_directions[id]
            final_x, final_y = current_x + MOVEMENTS[direction][0], current_y + MOVEMENTS[direction][1]
            if map[final_x][final_y] in [OUT_OF_BOUNDS_CELL, MOUNTAIN_CELL]:
                # move not allowed
                final_x, final_y = current_x, current_y
            bot_final_positions[id] = [final_x, final_y]

    return bot_final_positions

# Check if any two bots are crossing each other or reaching the same final position
# (DO NOT CHANGE THIS, YOUR CHANGES WILL BE IGNORED IN THE COMPETITION)
def bot_fights(bot_ids: dict, bot_current_positions: dict, bot_final_positions: dict, bot_food: dict):
    """
    Check if any two bots are crossing each other or reaching the same final position
    :param bot_ids: Dictionary containing the IDs of the bots
    :param bot_current_positions: Dictionary containing the current positions of the bots
    :param bot_final_positions: Dictionary containing the final positions of the bots
    :param bot_food: Dictionary containing the food count of the bots
    """
    final_pos_map = dict()
    current_pos_map = dict()
    for id in bot_ids.keys():
        if bot_ids[id] == BOT_ALIVE:
            current_pos_map[tuple(bot_current_positions[id])] = id     # Current position will be unique for every bot
            if tuple(bot_final_positions[id]) not in final_pos_map:
                final_pos_map[tuple(bot_final_positions[id])] = []
            final_pos_map[tuple(bot_final_positions[id])].append(id)
    
    # Check if any two bots are crossing each other
    for id in bot_ids.keys():
        if bot_ids[id] == BOT_ALIVE:
            if tuple(bot_final_positions[id]) in current_pos_map:  # Some bot is standing at the final position
                fighting_bot_id = current_pos_map[tuple(bot_final_positions[id])]
                if fighting_bot_id != id and bot_final_positions[fighting_bot_id] == bot_current_positions[id]:   # If bots are cross moving
                    # Fight
                    if bot_food[id] > bot_food[fighting_bot_id]:
                        bot_ids[fighting_bot_id] = BOT_DEAD
                        bot_food[id] += bot_food[fighting_bot_id]
                    else:
                        bot_ids[id] = BOT_DEAD
                        bot_food[fighting_bot_id] += bot_food[id]

    # Check if any two bots reaching the same final position
    for _, ids in final_pos_map.items():
        if len(ids) > 1:    # Fight
            strongest_bot = ids[0]
            for id in ids:
                if bot_ids[id] == BOT_ALIVE:
                    if bot_food[id] > bot_food[strongest_bot]:
                        strongest_bot = id
            
            for id in ids:
                if bot_ids[id] == BOT_ALIVE and id != strongest_bot:
                    bot_ids[id] = BOT_DEAD
                    bot_food[strongest_bot] += bot_food[id]

# Move the bots based on the directions they are moving
# (DO NOT CHANGE THIS, YOUR CHANGES WILL BE IGNORED IN THE COMPETITION)
def move_bots(map: list, bot_ids: dict, bot_current_positions: dict, bot_directions: dict, bot_food: dict):
    """
    Move the bots based on the directions they are moving
    :param map: The 2D map of the game
    :param bot_ids: Dictionary containing the IDs of the bots
    :param bot_current_positions: Dictionary containing the current positions of the bots
    :param bot_directions: Dictionary containing the directions in which the bots are moving
    :param bot_food: Dictionary containing the food count of the bots
    """
    bot_final_positions = calculate_final_bot_positions(map, bot_ids, bot_current_positions, bot_directions)
    bot_fights(bot_ids, bot_current_positions, bot_final_positions, bot_food)
    
    for id in bot_ids.keys():
        if bot_ids[id] == BOT_ALIVE:
            if map[bot_final_positions[id][0]][bot_final_positions[id][1]] == FOOD_CELL:
                bot_food[id] += 1

            if map[bot_current_positions[id][0]][bot_current_positions[id][1]] == str(id):
                map[bot_current_positions[id][0]][bot_current_positions[id][1]] = WALKABLE_CELL
            bot_current_positions[id] = bot_final_positions[id]   # Update the current position
            map[bot_final_positions[id][0]][bot_final_positions[id][1]] = str(id)    # Update the map

        else:
            if map[bot_current_positions[id][0]][bot_current_positions[id][1]] == str(id):
                map[bot_current_positions[id][0]][bot_current_positions[id][1]] = WALKABLE_CELL