import pygame
import random

# Initialize
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

# Snake
snake = [(100, 100)]
direction = (CELL_SIZE, 0)

# Food
def generate_food(snake):
    while True:
        x = random.randrange(0, WIDTH, CELL_SIZE)
        y = random.randrange(0, HEIGHT, CELL_SIZE)
        if (x, y) not in snake:
            return (x, y)

food = generate_food(snake)

# Game variables
score = 0
level = 1
speed = 7

running = True

while running:
    screen.fill(BLACK)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                direction = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN:
                direction = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT:
                direction = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT:
                direction = (CELL_SIZE, 0)

    # Move snake
    head_x, head_y = snake[0]
    new_head = (head_x + direction[0], head_y + direction[1])

    # ❌ Border collision
    if (
        new_head[0] < 0 or new_head[0] >= WIDTH or
        new_head[1] < 0 or new_head[1] >= HEIGHT
    ):
        print("Game Over (Wall)!")
        running = False

    # ❌ Self collision
    if new_head in snake:
        print("Game Over (Self)!")
        running = False

    snake.insert(0, new_head)

    # 🍎 Food eating
    if new_head == food:
        score += 1
        food = generate_food(snake)

        # 🎯 Level up every 4 points
        if score % 4 == 0:
            level += 1
            speed += 2
    else:
        snake.pop()

    # Draw snake
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))

    # Draw food
    pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))

    # Draw score and level
    text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()