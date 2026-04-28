# game.py
import pygame
import random
import sys
import json
import os
from db import save_result, get_personal_best

WIDTH = 600
HEIGHT = 600
CELL = 20
WALL = CELL

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (110, 110, 110)
LIGHT_GRAY = (220, 220, 220)
RED = (220, 20, 60)
DARK_RED = (120, 0, 0)
BLUE = (0, 100, 255)
ORANGE = (255, 140, 0)
PURPLE = (160, 32, 240)
CYAN = (0, 220, 220)
YELLOW = (255, 215, 0)

SETTINGS_FILE = "settings.json"


def load_settings():
    """Load game settings from settings.json."""
    default = {
        "snake_color": [0, 200, 0],
        "grid_overlay": True,
        "sound": True
    }

    if not os.path.exists(SETTINGS_FILE):
        save_settings(default)
        return default

    with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_settings(settings):
    """Save game settings to settings.json."""
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)


class SnakeGame:
    """Main Snake gameplay class."""

    def __init__(self, screen, username, settings):
        self.screen = screen
        self.username = username
        self.settings = settings

        self.font = pygame.font.SysFont("Verdana", 18)
        self.big_font = pygame.font.SysFont("Verdana", 48)

        self.snake_color = tuple(settings["snake_color"])
        self.grid_overlay = settings["grid_overlay"]

        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.dx = CELL
        self.dy = 0

        self.score = 0
        self.level = 1
        self.foods_eaten = 0
        self.base_speed = 7

        self.food_types = [
            {"weight": 1, "color": RED},
            {"weight": 2, "color": ORANGE},
            {"weight": 3, "color": BLUE},
        ]

        self.food_lifetime = 5000
        self.food = None
        self.food_spawn_time = 0

        self.poison = None
        self.poison_spawn_time = 0
        self.poison_lifetime = 7000

        self.power_up = None
        self.power_spawn_time = 0
        self.power_lifetime = 8000

        self.active_power = None
        self.power_end_time = 0
        self.shield = False

        self.obstacles = []

        self.personal_best = get_personal_best(username)

        self.game_over = False
        self.saved = False

        self.generate_food()
        self.generate_poison()

    def valid_position(self, pos):
        """Check if position is inside arena and not on snake or obstacles."""
        x, y = pos

        if x < WALL or x >= WIDTH - WALL:
            return False
        if y < WALL or y >= HEIGHT - WALL:
            return False
        if pos in self.snake:
            return False
        if pos in self.obstacles:
            return False

        return True

    def random_cell(self):
        """Return random cell inside the walls."""
        x = random.randrange(WALL, WIDTH - WALL, CELL)
        y = random.randrange(WALL, HEIGHT - WALL, CELL)
        return (x, y)

    def generate_food(self):
        """Generate weighted food with timer."""
        while True:
            pos = self.random_cell()

            if self.valid_position(pos):
                selected = random.choice(self.food_types).copy()
                selected["x"] = pos[0]
                selected["y"] = pos[1]
                self.food = selected
                self.food_spawn_time = pygame.time.get_ticks()
                break

    def generate_poison(self):
        """Generate poison food."""
        while True:
            pos = self.random_cell()

            if self.valid_position(pos) and (self.food is None or pos != (self.food["x"], self.food["y"])):
                self.poison = {"x": pos[0], "y": pos[1], "color": DARK_RED}
                self.poison_spawn_time = pygame.time.get_ticks()
                break

    def generate_power_up(self):
        """Generate one temporary power-up on field."""
        if self.power_up is not None:
            return

        power_types = [
            {"type": "speed", "color": CYAN, "label": "B"},
            {"type": "slow", "color": PURPLE, "label": "S"},
            {"type": "shield", "color": YELLOW, "label": "H"},
        ]

        while True:
            pos = self.random_cell()

            if self.valid_position(pos):
                selected = random.choice(power_types).copy()
                selected["x"] = pos[0]
                selected["y"] = pos[1]
                self.power_up = selected
                self.power_spawn_time = pygame.time.get_ticks()
                break

    def generate_obstacles(self):
        """Generate obstacle blocks from level 3."""
        if self.level < 3:
            return

        self.obstacles = []
        obstacle_count = min(5 + self.level, 20)

        protected = set()

        # Protect area around snake head so it does not get trapped
        head_x, head_y = self.snake[0]
        for dx in [-CELL, 0, CELL]:
            for dy in [-CELL, 0, CELL]:
                protected.add((head_x + dx, head_y + dy))

        attempts = 0

        while len(self.obstacles) < obstacle_count and attempts < 500:
            attempts += 1
            pos = self.random_cell()

            if pos in protected:
                continue
            if pos in self.snake:
                continue
            if self.food and pos == (self.food["x"], self.food["y"]):
                continue
            if self.poison and pos == (self.poison["x"], self.poison["y"]):
                continue
            if pos in self.obstacles:
                continue

            self.obstacles.append(pos)

    def update_level(self):
        """Increase level every 4 foods and create new obstacles."""
        old_level = self.level
        self.level = self.foods_eaten // 4 + 1

        if self.level != old_level:
            self.generate_obstacles()

    def current_speed(self):
        """Calculate snake speed with active power-up."""
        speed = self.base_speed + self.level - 1

        now = pygame.time.get_ticks()

        if self.active_power == "speed" and now < self.power_end_time:
            speed += 4
        elif self.active_power == "slow" and now < self.power_end_time:
            speed = max(3, speed - 4)
        elif self.active_power in ("speed", "slow") and now >= self.power_end_time:
            self.active_power = None

        return speed

    def handle_collision(self):
        """Handle wall, self, and obstacle collision."""
        head = self.snake[0]

        hit_wall = head[0] < WALL or head[0] >= WIDTH - WALL or head[1] < WALL or head[1] >= HEIGHT - WALL
        hit_self = head in self.snake[1:]
        hit_obstacle = head in self.obstacles

        if hit_wall or hit_self or hit_obstacle:
            if self.shield:
                self.shield = False
                self.active_power = None

                # Move snake back to safe position
                self.snake[0] = self.snake[1]
                return

            self.end_game()

    def shorten_snake(self, amount):
        """Shorten snake after eating poison."""
        for _ in range(amount):
            if len(self.snake) > 1:
                self.snake.pop()

        if len(self.snake) <= 1:
            self.end_game()

    def update(self):
        """Update game state."""
        now = pygame.time.get_ticks()

        # Timed food behavior
        if now - self.food_spawn_time > self.food_lifetime:
            self.generate_food()

        # Poison respawns after timer
        if self.poison is None or now - self.poison_spawn_time > self.poison_lifetime:
            self.generate_poison()

        # Power-up spawns randomly, only one on field
        if self.power_up is None and random.random() < 0.01:
            self.generate_power_up()

        # Power-up disappears after 8 seconds
        if self.power_up and now - self.power_spawn_time > self.power_lifetime:
            self.power_up = None

        head_x, head_y = self.snake[0]
        new_head = (head_x + self.dx, head_y + self.dy)

        self.snake.insert(0, new_head)

        self.handle_collision()

        if self.game_over:
            return

        ate_something = False

        # Eat normal weighted food
        if new_head == (self.food["x"], self.food["y"]):
            self.score += self.food["weight"]
            self.foods_eaten += 1
            self.update_level()
            self.generate_food()
            ate_something = True

        # Eat poison
        if self.poison and new_head == (self.poison["x"], self.poison["y"]):
            self.shorten_snake(2)
            self.poison = None
            ate_something = True

        # Collect power-up
        if self.power_up and new_head == (self.power_up["x"], self.power_up["y"]):
            p_type = self.power_up["type"]

            if p_type == "speed":
                self.active_power = "speed"
                self.power_end_time = now + 5000

            elif p_type == "slow":
                self.active_power = "slow"
                self.power_end_time = now + 5000

            elif p_type == "shield":
                self.active_power = "shield"
                self.shield = True

            self.power_up = None

        if not ate_something:
            self.snake.pop()

    def change_direction(self, key):
        """Change snake direction and prevent reverse movement."""
        if key == pygame.K_UP and self.dy == 0:
            self.dx = 0
            self.dy = -CELL
        elif key == pygame.K_DOWN and self.dy == 0:
            self.dx = 0
            self.dy = CELL
        elif key == pygame.K_LEFT and self.dx == 0:
            self.dx = -CELL
            self.dy = 0
        elif key == pygame.K_RIGHT and self.dx == 0:
            self.dx = CELL
            self.dy = 0

    def draw_walls(self):
        """Draw border walls."""
        pygame.draw.rect(self.screen, GRAY, (0, 0, WIDTH, WALL))
        pygame.draw.rect(self.screen, GRAY, (0, HEIGHT - WALL, WIDTH, WALL))
        pygame.draw.rect(self.screen, GRAY, (0, 0, WALL, HEIGHT))
        pygame.draw.rect(self.screen, GRAY, (WIDTH - WALL, 0, WALL, HEIGHT))

    def draw_grid(self):
        """Draw optional grid overlay."""
        if not self.grid_overlay:
            return

        for x in range(WALL, WIDTH - WALL, CELL):
            pygame.draw.line(self.screen, LIGHT_GRAY, (x, WALL), (x, HEIGHT - WALL), 1)

        for y in range(WALL, HEIGHT - WALL, CELL):
            pygame.draw.line(self.screen, LIGHT_GRAY, (WALL, y), (WIDTH - WALL, y), 1)

    def draw_snake(self):
        """Draw snake."""
        for segment in self.snake:
            pygame.draw.rect(self.screen, self.snake_color, (segment[0], segment[1], CELL, CELL))

    def draw_food(self):
        """Draw weighted food."""
        pygame.draw.rect(self.screen, self.food["color"], (self.food["x"], self.food["y"], CELL, CELL))
        text = self.font.render(str(self.food["weight"]), True, WHITE)
        self.screen.blit(text, (self.food["x"] + 4, self.food["y"] - 3))

    def draw_poison(self):
        """Draw poison food."""
        if self.poison:
            pygame.draw.rect(self.screen, self.poison["color"], (self.poison["x"], self.poison["y"], CELL, CELL))
            text = self.font.render("P", True, WHITE)
            self.screen.blit(text, (self.poison["x"] + 4, self.poison["y"] - 3))

    def draw_power_up(self):
        """Draw power-up item."""
        if self.power_up:
            pygame.draw.rect(self.screen, self.power_up["color"], (self.power_up["x"], self.power_up["y"], CELL, CELL))
            text = self.font.render(self.power_up["label"], True, BLACK)
            self.screen.blit(text, (self.power_up["x"] + 4, self.power_up["y"] - 3))

    def draw_obstacles(self):
        """Draw obstacle blocks."""
        for block in self.obstacles:
            pygame.draw.rect(self.screen, BLACK, (block[0], block[1], CELL, CELL))

    def draw_info(self):
        """Draw game information."""
        now = pygame.time.get_ticks()
        food_timer = max(0, (self.food_lifetime - (now - self.food_spawn_time)) // 1000)

        texts = [
            f"Player: {self.username}",
            f"Score: {self.score}",
            f"Level: {self.level}",
            f"Best: {self.personal_best}",
            f"Food timer: {food_timer}"
        ]

        y = 5
        for item in texts:
            surface = self.font.render(item, True, BLACK)
            self.screen.blit(surface, (25, y))
            y += 22

        if self.active_power == "speed":
            rem = max(0, (self.power_end_time - now) // 1000)
            power_text = f"Power: Speed {rem}s"
        elif self.active_power == "slow":
            rem = max(0, (self.power_end_time - now) // 1000)
            power_text = f"Power: Slow {rem}s"
        elif self.shield:
            power_text = "Power: Shield"
        else:
            power_text = "Power: None"

        surface = self.font.render(power_text, True, BLUE)
        self.screen.blit(surface, (360, 5))

    def draw(self):
        """Draw everything."""
        self.screen.fill(WHITE)
        self.draw_grid()
        self.draw_walls()
        self.draw_obstacles()
        self.draw_snake()
        self.draw_food()
        self.draw_poison()
        self.draw_power_up()
        self.draw_info()

    def end_game(self):
        """End game and save result once."""
        self.game_over = True

        if not self.saved:
            save_result(self.username, self.score, self.level)
            self.saved = True
