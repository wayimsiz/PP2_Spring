import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Chase")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

clock = pygame.time.Clock()

# Игрок
radius = 11
step = 4

x = 40
y = 40

# Враг
enemy_size = 16
enemy_speed = 2

enemy_x = 740
enemy_y = 540

# Финиш — там же где появляется враг
finish_size = 30
finish_x = enemy_x
finish_y = enemy_y

# стены
walls = [

    pygame.Rect(0, 0, 20, 250),
    pygame.Rect(150, 350, 20, 250),

    pygame.Rect(300, 150, 20, 100),

    pygame.Rect(450, 0, 20, 250),
    pygame.Rect(450, 350, 20, 250),

    pygame.Rect(6, 150, 20, 450),

    pygame.Rect(0, 120, 250, 20),
    pygame.Rect(350, 120, 450, 20),

    pygame.Rect(0, 300, 450, 20),
    pygame.Rect(0, 30, 25, 100),

    pygame.Rect(0, 480, 650, 20),
]


def can_move_circle(new_x, new_y):

    rect = pygame.Rect(
        new_x - radius,
        new_y - radius,
        radius * 2,
        radius * 2
    )

    for wall in walls:
        if rect.colliderect(wall):
            return False

    return True


def can_move_enemy(new_x, new_y):

    rect = pygame.Rect(
        new_x,
        new_y,
        enemy_size,
        enemy_size
    )

    for wall in walls:
        if rect.colliderect(wall):
            return False

    return True


running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    new_x = x
    new_y = y

    if keys[pygame.K_UP]:
        new_y -= step

    if keys[pygame.K_DOWN]:
        new_y += step

    if keys[pygame.K_LEFT]:
        new_x -= step

    if keys[pygame.K_RIGHT]:
        new_x += step

    if (
        new_x - radius >= 0 and
        new_x + radius <= WIDTH and
        new_y - radius >= 0 and
        new_y + radius <= HEIGHT and
        can_move_circle(new_x, new_y)
    ):
        x = new_x
        y = new_y

    # Движение врага
    enemy_new_x = enemy_x

    if enemy_x < x:
        enemy_new_x += enemy_speed
    elif enemy_x > x:
        enemy_new_x -= enemy_speed

    if can_move_enemy(enemy_new_x, enemy_y):
        enemy_x = enemy_new_x

    enemy_new_y = enemy_y

    if enemy_y < y:
        enemy_new_y += enemy_speed
    elif enemy_y > y:
        enemy_new_y -= enemy_speed

    if can_move_enemy(enemy_x, enemy_new_y):
        enemy_y = enemy_new_y

    player_rect = pygame.Rect(
        x - radius,
        y - radius,
        radius * 2,
        radius * 2
    )

    enemy_rect = pygame.Rect(
        enemy_x,
        enemy_y,
        enemy_size,
        enemy_size
    )

    if player_rect.colliderect(enemy_rect):
        print("\033[31mGame Over!\033[0m")
        running = False

    finish_rect = pygame.Rect(
        finish_x,
        finish_y,
        finish_size,
        finish_size
    )

    if player_rect.colliderect(finish_rect):
        print("\033[32mYou Win!\033[0m")
        running = False

    screen.fill(WHITE)

    for wall in walls:
        pygame.draw.rect(screen, BLACK, wall)

    pygame.draw.circle(
        screen,
        RED,
        (x, y),
        radius
    )

    pygame.draw.rect(
        screen,
        BLUE,
        (enemy_x, enemy_y, enemy_size, enemy_size)
    )

    pygame.draw.rect(
        screen,
        GREEN,
        (finish_x, finish_y, finish_size, finish_size)
    )

    pygame.display.flip()

    clock.tick(60)

pygame.quit()