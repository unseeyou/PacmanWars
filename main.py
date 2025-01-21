import pygame
from constants import *
from map_generator import generate_map
from food_generator import generate_food
from player_generator import generate_player
from bots.bot import Bot

pygame.init()
screen = pygame.display.set_mode((HEIGHT, WIDTH))
pygame.display.set_caption("PACMAN WARS")

def draw_grid_map(screen, map):
    font = pygame.font.SysFont(None, 18)
    for i, row in enumerate(map):
        for j, cell in enumerate(row):
            if cell in COLOR_MAP.keys():
                color = COLOR_MAP[cell]
            else:
                color = COLOR_MAP[PLAYER_CELL]
            pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

            if cell not in COLOR_MAP.keys():
                text = font.render(cell, True, BLACK)
                screen.blit(text, (j * CELL_SIZE + CELL_SIZE // 3, i * CELL_SIZE + CELL_SIZE // 4))

def get_minimap(map, x, y):
    minimap = [row[y - 2: y+3] for row in map[x - 2: x+3]]
    return minimap

def load_bots(players: dict, map: list):
    bots = []
    for bot in range(1, len(players.keys())+1):
        bots.append(Bot(bot, players[bot][0], players[bot][1], get_minimap(map, players[bot][0], players[bot][1])))
    return bots

def move_player(map:list, players: dict, player: int, direction: int):
    x, y = players[player]
    map[x][y] = WALKABLE_CELL
    if direction == 0 and map[x-1][y] == WALKABLE_CELL:  # up
        x -= 1
    elif direction == 1 and map[x+1][y] == WALKABLE_CELL: # down
        x += 1
    elif direction == 2 and map[x][y-1] == WALKABLE_CELL: # left
        y -= 1
    elif direction == 3 and map[x][y+1] == WALKABLE_CELL: # right
        y += 1
    map[x][y] = str(player)
    players[player] = (x, y)

def main():
    clock = pygame.time.Clock()
    map = generate_map(0.8, 0.6, 200)
    players = generate_player(map, 40)
    users = load_bots(players, map)

    is_game_running = True
    while is_game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_game_running = False
        
        for ind, user in enumerate(users):
            move_player(map, players, ind+1, user.move(get_minimap(map, players[ind+1][0], players[ind+1][1])))

        draw_grid_map(screen, map)
        generate_food(map, 5)
        pygame.display.flip()
        clock.tick(1)

if __name__ == "__main__":
    main()