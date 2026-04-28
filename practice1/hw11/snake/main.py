import pygame
import random
import sys
import time

pygame.init()

# Screen settings
WIDTH = 600
HEIGHT = 600
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game with Weighted Food")

clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (100, 100, 100)
BLUE = (0, 0, 200)
ORANGE = (255, 140, 0)
PURPLE = (160, 32, 240)

# Fonts
font = pygame.font.SysFont("Verdana", 20)
game_over_font = pygame.font.SysFont("Verdana", 50)

# Game area borders
WALL_THICKNESS = CELL

# Snake settings
snake = [(100, 100), (80, 100), (60, 100)]
dx = CELL
dy = 0

# Score and level
score = 0
level = 1
foods_eaten = 0
base_speed = 7

# Food disappears after this number of seconds
FOOD_LIFETIME = 5
food_spawn_time = 0

# Different food types with different weights
food_types = [
    {"weight": 1, "color": RED},
    {"weight": 2, "color": ORANGE},
    {"weight": 3, "color": BLUE},
    {"weight": 5, "color": PURPLE},
]

food = None


def draw_walls():
    """Draw borders around the game area."""
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, WALL_THICKNESS))
    pygame.draw.rect(screen, GRAY, (0, HEIGHT - WALL_THICKNESS, WIDTH, WALL_THICKNESS))
    pygame.draw.rect(screen, GRAY, (0, 0, WALL_THICKNESS, HEIGHT))
    pygame.draw.rect(screen, GRAY, (WIDTH - WALL_THICKNESS, 0, WALL_THICKNESS, HEIGHT))


def draw_snake():
    """Draw every snake segment."""
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL, CELL))


def draw_food():
    """Draw food and show its weight."""
    pygame.draw.rect(screen, food["color"], (food["x"], food["y"], CELL, CELL))

    # Write food weight inside the food block
    weight_text = font.render(str(food["weight"]), True, WHITE)
    screen.blit(weight_text, (food["x"] + 4, food["y"] - 2))


def draw_info():
    """Draw score, level, speed, and food timer."""
    score_text = font.render(f"Score: {score}", True, BLACK)
    level_text = font.render(f"Level: {level}", True, BLACK)
    speed_text = font.render(f"Speed: {base_speed + level - 1}", True, BLACK)

    remaining_time = max(0, FOOD_LIFETIME - int(time.time() - food_spawn_time))
    timer_text = font.render(f"Food timer: {remaining_time}", True, BLACK)

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 35))
    screen.blit(speed_text, (10, 60))
    screen.blit(timer_text, (10, 85))


def generate_food():
    """Generate random food that does not appear on walls or snake."""
    global food_spawn_time

    while True:
        x = random.randrange(CELL, WIDTH - CELL, CELL)
        y = random.randrange(CELL, HEIGHT - CELL, CELL)

        # Food must not appear on snake
        if (x, y) not in snake:
            selected_food = random.choice(food_types).copy()
            selected_food["x"] = x
            selected_food["y"] = y

            # Save time when food appeared
            food_spawn_time = time.time()

            return selected_food


def check_wall_collision(position):
    """Check if snake hits the wall."""
    x, y = position

    if x < CELL or x >= WIDTH - CELL:
        return True
    if y < CELL or y >= HEIGHT - CELL:
        return True

    return False


def check_self_collision():
    """Check if snake hits itself."""
    head = snake[0]
    return head in snake[1:]


def update_level():
    """Increase level after every 4 eaten foods."""
    global level
    level = foods_eaten // 4 + 1


def show_game_over():
    """Show Game Over screen."""
    screen.fill(WHITE)

    text = game_over_font.render("Game Over", True, RED)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))

    final_score = font.render(f"Final Score: {score}", True, BLACK)
    score_rect = final_score.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))

    screen.blit(text, text_rect)
    screen.blit(final_score, score_rect)

    pygame.display.flip()
    pygame.time.delay(3000)


food = generate_food()

running = True

while running:
    clock.tick(base_speed + level - 1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Prevent snake from moving directly backward
            if event.key == pygame.K_UP and dy == 0:
                dx = 0
                dy = -CELL
            elif event.key == pygame.K_DOWN and dy == 0:
                dx = 0
                dy = CELL
            elif event.key == pygame.K_LEFT and dx == 0:
                dx = -CELL
                dy = 0
            elif event.key == pygame.K_RIGHT and dx == 0:
                dx = CELL
                dy = 0

    # If food is not eaten in time, it disappears and new food appears
    if time.time() - food_spawn_time > FOOD_LIFETIME:
        food = generate_food()

    # Move snake
    head_x, head_y = snake[0]
    new_head = (head_x + dx, head_y + dy)

    # Check wall collision
    if check_wall_collision(new_head):
        show_game_over()
        break

    snake.insert(0, new_head)

    # Check if food is eaten
    if new_head == (food["x"], food["y"]):
        score += food["weight"]
        foods_eaten += 1
        update_level()
        food = generate_food()
    else:
        snake.pop()

    # Check self collision
    if check_self_collision():
        show_game_over()
        break

    # Draw everything
    screen.fill(WHITE)
    draw_walls()
    draw_snake()
    draw_food()
    draw_info()
    pygame.display.flip()

pygame.quit()
sys.exit()