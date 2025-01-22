import pygame
from constants import *
from map_generator import generate_map
from food_generator import generate_food
from bot_operations import get_number_of_bots, generate_bot_positions, load_bots, move_bots, get_minimap

# Initialize the game using pygame UI
pygame.init()
screen = pygame.display.set_mode((HEIGHT, WIDTH))
pygame.display.set_caption("PACMAN WARS")

# Draw the game snapshot on the screen
# (DO NOT CHANGE THIS, YOUR CHANGES WILL BE IGNORED IN THE COMPETITION)
def draw_grid_map(screen: pygame.Surface, map: list):
    """
    Draw the grid map on the screen
    :param screen: UI screen
    :param map: 2D list representing the game map
    """
    font = pygame.font.SysFont(None, 18)
    for i, row in enumerate(map):
        for j, cell in enumerate(row):
            if cell in COLOR_MAP.keys():    # If its not a player cell
                color = COLOR_MAP[cell]
            else:   # Player cell will be marked by a number rather than 'P'
                color = COLOR_MAP[PLAYER_CELL]
            
            # Draw the cell with desired color
            pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

            # If its a player cell, draw the player number
            if cell not in COLOR_MAP.keys():
                text = font.render(cell, True, BLACK)
                screen.blit(text, (j * CELL_SIZE + CELL_SIZE // 3, i * CELL_SIZE + CELL_SIZE // 4))

# Execute bot code to find the next move
# (DO NOT CHANGE THIS, YOUR CHANGES WILL BE IGNORED IN THE COMPETITION)
def calculate_bot_directions(map: list, bots: dict, bot_positions: dict, bot_ids: dict) -> dict:
    """
    Calculate the next move for each bot
    :param map: 2D list representing the game map
    :param bots: Dictionary containing bot objects
    :param bot_positions: Dictionary containing bot positions
    :param bot_ids: Dictionary containing bot ids
    """
    bot_directions = {}
    for id, bot in bots.items():
        if bot_ids[id] == BOT_ALIVE:
            bot_directions[id] = bot.move(
                current_x=bot_positions[id][0],
                current_y=bot_positions[id][1],
                minimap=get_minimap(map, bot_positions[id][0], bot_positions[id][1]))
    return bot_directions

def main():
    clock = pygame.time.Clock()
    map = generate_map(0.6, 0.6, 200)   # Generate the game map
    number_of_bots = get_number_of_bots()   # Get the number of bots
    bot_positions = generate_bot_positions(map, number_of_bots)  # Generate the bot positions
    bots, bot_names = load_bots(bot_positions, map) # Generate bot objects with names
    bot_food = {id: 1 for id in bot_positions.keys()}  # Initialize the food count for each bot
    bot_ids = {id: BOT_ALIVE for id in range(1, number_of_bots + 1)} # Initialize the bot ids with BOT_ALIVE status

    is_game_running = True  # Game loop
    while is_game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_game_running = False
        
        bot_directions = calculate_bot_directions(map, bots, bot_positions, bot_ids)
        move_bots(map, bot_ids, bot_positions, bot_directions, bot_food)

        draw_grid_map(screen, map)
        generate_food(map, 5)
        pygame.display.flip()
        clock.tick(1)

if __name__ == "__main__":
    main()