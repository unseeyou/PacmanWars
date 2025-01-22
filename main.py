import pygame
from constants import *
from map_generator import generate_map
from food_generator import generate_food
from bot_operations import *

# Initialize the game using pygame UI
pygame.init()
screen = pygame.display.set_mode((WIDTH + 200, HEIGHT + 100))
pygame.display.set_caption("PACMAN WARS")

def draw_title(screen: pygame.Surface):
    """
    Draw the title on the screen
    :param screen: UI screen
    """
    font = pygame.font.SysFont('Arial', 45, bold=True)  # Use Arial font with size 30 and bold
    text = font.render("PACMAN WARS", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 20))

def draw_game_over(screen: pygame.Surface, winner_bot_name: str):
    """
    Draw the game over on the screen
    :param screen: UI screen
    :param winner_bot_name: Name of the winner bot
    """
    font = pygame.font.SysFont('Arial', 50, bold=True)  # Use Arial font with size 30 and bold
    text = font.render("GAME OVER", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2 + 100, HEIGHT // 2))
    text = font.render(f"WINNER IS {winner_bot_name}", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2 + 100, HEIGHT // 2 + 100))

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
            pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE + 100, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (j * CELL_SIZE, i * CELL_SIZE + 100, CELL_SIZE, CELL_SIZE), 1)

            # If its a player cell, draw the player number
            if cell not in COLOR_MAP.keys():
                text = font.render(cell, True, BLACK)
                screen.blit(text, (j * CELL_SIZE + CELL_SIZE // 3, i * CELL_SIZE + 100 + CELL_SIZE // 4))

def draw_moves_left(screen: pygame.Surface, moves_left: int):
    """
    Draw the number of moves left on the screen
    :param screen: UI screen
    :param moves_left: Number of moves left for game to end
    """
    font = pygame.font.SysFont('Arial', 25, bold=True)  # Use Arial font with size 30 and bold
    text = font.render(f"Moves left : {moves_left}", True, WHITE)
    screen.blit(text, (WIDTH + 20, 20))

def draw_scoreboard(screen: pygame.Surface, bot_food: dict, bot_names: dict):
    """
    Draw the scoreboard on the screen
    :param screen: UI screen
    :param bot_food: Dictionary containing the food count of the bots
    :param bot_names: Dictionary containing the names of the bots
    """
    font = pygame.font.SysFont('Arial', 20, bold=False)  # Use Arial font with size 20 and not bold
    sorted_bots = sorted(bot_food.items(), key=lambda item: item[1], reverse=True)
    
    x_offset = WIDTH + 20
    y_offset = 120
    scoreboard_width = 180
    scoreboard_height = 40 + len(sorted_bots) * 30

    # Draw the box around the scoreboard
    pygame.draw.rect(screen, WHITE, (x_offset - 10, y_offset - 10, scoreboard_width, scoreboard_height), 2)

    screen.blit(font.render("Scoreboard", True, WHITE), (x_offset, y_offset))
    y_offset += 30
    
    for bot_id, food in sorted_bots:
        bot_name = bot_names[bot_id]
        text = f"{bot_name}: {food}"
        screen.blit(font.render(text, True, WHITE), (x_offset, y_offset))
        y_offset += 30

def main():
    clock = pygame.time.Clock()
    map = generate_map(0.6, 0.6, 200)   # Generate the game map
    number_of_bots = get_number_of_bots()   # Get the number of bots
    bot_positions = generate_bot_positions(map, number_of_bots)  # Generate the bot positions
    bots, bot_names = load_bots(bot_positions, map) # Generate bot objects with names
    bot_food = {id: 1 for id in bot_positions.keys()}  # Initialize the food count for each bot
    bot_ids = {id: BOT_ALIVE for id in range(1, number_of_bots + 1)} # Initialize the bot ids with BOT_ALIVE status

    is_game_running = True  # Game loop
    game_counter = 1000 # Maximum game moves
    while is_game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_game_running = False

        if game_counter > 0:
            bot_directions = calculate_bot_directions(map, bots, bot_positions, bot_ids, bot_food)
            move_bots(map, bot_ids, bot_positions, bot_directions, bot_food)

            screen.fill(BLACK)
            draw_title(screen)
            draw_grid_map(screen, map)
            draw_scoreboard(screen, bot_food, bot_names)
            draw_moves_left(screen, game_counter)
            generate_food(map, number_of_bots)
        
        else:
            winner = 1
            for id in bot_food.keys():
                if bot_food[id] > bot_food[winner]:
                    winner = id
            screen.fill(BLACK)
            draw_game_over(screen, bot_names[id])
        
        game_counter -= 1
        pygame.display.flip()
        clock.tick(1)

if __name__ == "__main__":
    main()