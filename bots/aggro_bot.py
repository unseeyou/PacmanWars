import random
from collections import deque
from bots.bot import Bot
from constants import *

class AggroBot(Bot):
    def __init__(self, id: int, start_x: int, start_y: int, minimap: list, map_length: int, map_breadth: int):
        super().__init__(id, start_x, start_y, minimap, map_length, map_breadth)
        self.move_history = [] 
        self.last_position = None

    def move(self, current_x: int, current_y: int, minimap: list, bot_food: dict) -> int:
        self.update_state(current_x, current_y, minimap, bot_food)
        
        self.last_position = (current_x, current_y)
        
        threat_move = self.avoid_threats()
        if threat_move is not None:
            self.move_history.append((current_x, current_y, "avoid_threat"))
            return threat_move

        if len(self.move_history) >= 8:
            recent_positions = [(x, y) for x, y, _ in self.move_history[-8:]]
            unique_positions = len(set(recent_positions))
            if unique_positions <= 4:
                kill_move = self.bfs_for_weaker_bot(extended_range=True)
                if kill_move is not None:
                    self.move_history.append((current_x, current_y, "hunt"))
                    return kill_move
                explore_move = self._get_exploration_move(force_explore=True)
                if explore_move is not None:
                    self.move_history.append((current_x, current_y, "explore"))
                    return explore_move

        surrounded_by_food = True
        for dx, dy in MOVEMENTS.values():
            nx, ny = self.x + dx, self.y + dy
            if self._in_bounds(nx, ny) and self.map[nx][ny] != FOOD_CELL:
                surrounded_by_food = False
                break

        if surrounded_by_food:
            kill_move = self.bfs_for_weaker_bot(extended_range=True)
            if kill_move is not None:
                self.move_history.append((current_x, current_y, "hunt"))
                return kill_move
            explore_move = self._get_exploration_move()
            if explore_move is not None:
                self.move_history.append((current_x, current_y, "explore"))
                return explore_move

        kill_move = self.bfs_for_weaker_bot()
        if kill_move is not None:
            self.move_history.append((current_x, current_y, "hunt"))
            return kill_move

        food_move = self.bfs_for_food()
        if food_move is not None:
            self.move_history.append((current_x, current_y, "seek_food"))
            return food_move

        self.move_history.append((current_x, current_y, "random"))
        return self._get_random_move()

    def avoid_threats(self) -> int:
        my_food = self.bot_food.get(self.id, 1)

        directions = {
            MOVE_UP:    (self.x - 1, self.y),
            MOVE_DOWN:  (self.x + 1, self.y),
            MOVE_LEFT:  (self.x, self.y - 1),
            MOVE_RIGHT: (self.x, self.y + 1)
        }

        threats = []
        safe_moves = []
        for dir_constant, (nx, ny) in directions.items():
            if not self._in_bounds(nx, ny):
                continue
            cell_val = self.map[nx][ny]
            if cell_val not in [WALKABLE_CELL, FOOD_CELL, MOUNTAIN_CELL, OUT_OF_BOUNDS_CELL, UNKNOWN_CELL]:
                try:
                    other_bot_id = int(cell_val)
                    if self.bot_food.get(other_bot_id, 1) >= my_food:
                        threats.append(dir_constant)
                    continue
                except ValueError:
                    pass
            if cell_val in [WALKABLE_CELL, FOOD_CELL]:
                safe_moves.append(dir_constant)

        if not threats:
            return None

        if len(threats) >= 3 and not safe_moves:
            return MOVE_HALT

        opposite = {
            MOVE_UP: MOVE_DOWN,
            MOVE_DOWN: MOVE_UP,
            MOVE_LEFT: MOVE_RIGHT,
            MOVE_RIGHT: MOVE_LEFT
        }
        threat_dir = threats[0]

        escape_dir = opposite[threat_dir]

        safe_dirs = [d for d in MOVEMENTS.keys() if d != threat_dir]
        for safe_dir in safe_dirs:
            dx, dy = MOVEMENTS[safe_dir]
            ex, ey = self.x + dx, self.y + dy
            if self._in_bounds(ex, ey) and self.map[ex][ey] == FOOD_CELL:
                return safe_dir

        dx, dy = MOVEMENTS[escape_dir]
        ex, ey = self.x + dx, self.y + dy
        if self._in_bounds(ex, ey) and self.map[ex][ey] in [WALKABLE_CELL, FOOD_CELL]:
            return escape_dir

        return safe_moves[0] if safe_moves else MOVE_HALT

    def _get_random_move(self) -> int:
        cycle_length = 4
        if len(self.move_history) >= cycle_length * 2:
            recent_positions = [(x, y) for x, y, _ in self.move_history[-cycle_length:]]
            if recent_positions in [[(x, y) for x, y, _ in self.move_history[-cycle_length*2:-cycle_length]]]:
                available_moves = []
                for move in [MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT]:
                    dx, dy = MOVEMENTS[move]
                    nx, ny = self.x + dx, self.y + dy
                    if self._in_bounds(nx, ny) and (nx, ny) not in recent_positions:
                        available_moves.append(move)
                if available_moves:
                    return random.choice(available_moves)

        available_moves = []
        for move in [MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT]:
            dx, dy = MOVEMENTS[move]
            nx, ny = self.x + dx, self.y + dy
            if not self._in_bounds(nx, ny):
                continue
            if self.map[nx][ny] in [WALKABLE_CELL, FOOD_CELL]:
                if self.last_position and (nx, ny) != self.last_position:
                    available_moves.append(move)

        if available_moves:
            return random.choice(available_moves)

        valid_moves = [move for move in [MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT]
                      if self._in_bounds(self.x + MOVEMENTS[move][0], 
                                       self.y + MOVEMENTS[move][1])]
        return random.choice(valid_moves) if valid_moves else MOVE_UP

    def _get_exploration_move(self, force_explore=False) -> int:
        if len(self.move_history) < 4 and not force_explore:
            return None

        recent_positions = [(x, y) for x, y, _ in self.move_history[-8:]]
        center_x = sum(x for x, _ in recent_positions) / len(recent_positions)
        center_y = sum(y for _, y in recent_positions) / len(recent_positions)

        best_move = None
        max_distance = -1

        for move in [MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT]:
            dx, dy = MOVEMENTS[move]
            nx, ny = self.x + dx, self.y + dy
            if not self._in_bounds(nx, ny):
                continue
            if self.map[nx][ny] not in [MOUNTAIN_CELL, OUT_OF_BOUNDS_CELL, UNKNOWN_CELL]:
                position_penalty = 2 if (nx, ny) in recent_positions else 0
                distance = ((nx - center_x) ** 2 + (ny - center_y) ** 2) ** 0.5 - position_penalty
                if distance > max_distance:
                    max_distance = distance
                    best_move = move

        return best_move if best_move is not None else random.choice(list(MOVEMENTS.keys()))

    def bfs_for_weaker_bot(self, extended_range=False):
        my_food = self.bot_food.get(self.id, 1)
        max_depth = 15 if extended_range else 5
        return self._bfs_for_target(
            is_target_fn=lambda cell_val: self._is_killable_bot(cell_val, my_food),
            max_depth=max_depth
        )

    def bfs_for_food(self):
        def calculate_food_density(x, y):
            density = 0
            for dx in [-2, -1, 0, 1, 2]:
                for dy in [-2, -1, 0, 1, 2]:
                    nx, ny = x + dx, y + dy
                    if self._in_bounds(nx, ny) and self.map[nx][ny] == FOOD_CELL:
                        density += 1
            return density

        return self._bfs_for_target(
            is_target_fn=lambda cell_val: (cell_val == FOOD_CELL),
            score_fn=calculate_food_density
        )

    def _bfs_for_target(self, is_target_fn, score_fn=None, max_depth=5):
        visited = set()
        queue = deque()
        queue.append((self.x, self.y, None, 0))
        visited.add((self.x, self.y))
        targets = []

        while queue:
            cx, cy, first_dir, depth = queue.popleft()
            if depth > max_depth:
                continue

            cell_val = self.map[cx][cy]

            if is_target_fn(cell_val):
                food_on_path = self._count_food_on_path(self.x, self.y, cx, cy)
                score = (score_fn(cx, cy) if score_fn else 1) + food_on_path * 0.5
                targets.append((cx, cy, first_dir, score))
                continue

            for d, (dx, dy) in MOVEMENTS.items():
                nx, ny = cx + dx, cy + dy
                if not self._in_bounds(nx, ny):
                    continue
                if (nx, ny) not in visited and self.map[nx][ny] in [WALKABLE_CELL, FOOD_CELL] + self._possible_bot_cells():
                    visited.add((nx, ny))
                    next_dir = first_dir if first_dir is not None else d
                    queue.append((nx, ny, next_dir, depth + 1))

        if targets:
            best_target = max(targets, key=lambda t: t[3])
            if best_target[2] is None:
                valid_dirs = []
                for d, (dx, dy) in MOVEMENTS.items():
                    nx, ny = self.x + dx, self.y + dy
                    if self._in_bounds(nx, ny) and self.map[nx][ny] in [WALKABLE_CELL, FOOD_CELL]:
                        valid_dirs.append(d)
                if valid_dirs:
                    return random.choice(valid_dirs)
            return best_target[2]

        return None

    def _count_food_on_path(self, start_x, start_y, target_x, target_y):
        food_count = 0
        x, y = start_x, start_y
        while x != target_x or y != target_y:
            if x < target_x:
                x += 1
            elif x > target_x:
                x -= 1
            if y < target_y:
                y += 1
            elif y > target_y:
                y -= 1
            if self._in_bounds(x, y) and self.map[x][y] == FOOD_CELL:
                food_count += 1
        return food_count

    def _in_bounds(self, x, y) -> bool:
        return 0 <= x < len(self.map) and 0 <= y < len(self.map[0])

    def _is_killable_bot(self, cell_val, my_food):
        if cell_val in [WALKABLE_CELL, FOOD_CELL, MOUNTAIN_CELL, OUT_OF_BOUNDS_CELL, UNKNOWN_CELL]:
            return False
        try:
            other_bot_id = int(cell_val)
            if other_bot_id == self.id:
                return False
            other_food = self.bot_food.get(other_bot_id, 1)
            return (other_food < my_food)
        except ValueError:
            return False

    def _possible_bot_cells(self):
        my_food = self.bot_food.get(self.id, 1)
        return [
            str(bot_id) 
            for bot_id, food_count in self.bot_food.items() 
            if food_count <= my_food and bot_id != self.id
        ]
