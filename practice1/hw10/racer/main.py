import sys
import random
import pygame
from pygame.locals import *

# -----------------------------
# INITIALIZATION
# -----------------------------
pygame.init()

# -----------------------------
# GAME SETTINGS
# -----------------------------
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60
SPEED = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)
DARK_GRAY = (60, 60, 60)
RED = (220, 20, 60)
BLUE = (50, 130, 255)
YELLOW = (255, 215, 0)
GREEN = (0, 200, 120)

# Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer without Images")

# Clock
clock = pygame.time.Clock()

# Fonts
font_small = pygame.font.SysFont("Verdana", 20)
font_big = pygame.font.SysFont("Verdana", 42)

# Game variables
score = 0
coins_collected = 0


# -----------------------------
# BACKGROUND CLASS
# Draws road and moving lane lines
# -----------------------------
class Road:
    def __init__(self):
        self.line_y = 0

    def update(self):
        """Move lane markings downward."""
        self.line_y += SPEED
        if self.line_y >= 40:
            self.line_y = 0

    def draw(self, surface):
        """Draw the road background."""
        # Grass / side area
        surface.fill(GREEN)

        # Main road
        pygame.draw.rect(surface, DARK_GRAY, (50, 0, 300, SCREEN_HEIGHT))

        # Road borders
        pygame.draw.line(surface, WHITE, (50, 0), (50, SCREEN_HEIGHT), 4)
        pygame.draw.line(surface, WHITE, (350, 0), (350, SCREEN_HEIGHT), 4)

        # Middle dashed lines
        for y in range(-40, SCREEN_HEIGHT, 40):
            pygame.draw.rect(surface, WHITE, (195, y + self.line_y, 10, 25))


# -----------------------------
# PLAYER CLASS
# -----------------------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 40
        self.height = 70
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.draw_car(self.image, BLUE)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))

    def draw_car(self, surface, color):
        """Draw a simple car shape."""
        pygame.draw.rect(surface, color, (5, 10, 30, 50), border_radius=8)
        pygame.draw.rect(surface, BLACK, (10, 15, 20, 15), border_radius=4)

        # Wheels
        pygame.draw.circle(surface, BLACK, (8, 18), 5)
        pygame.draw.circle(surface, BLACK, (32, 18), 5)
        pygame.draw.circle(surface, BLACK, (8, 52), 5)
        pygame.draw.circle(surface, BLACK, (32, 52), 5)

    def move(self):
        """Move player left and right."""
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-6, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(6, 0)

        # Keep player inside road
        if self.rect.left < 55:
            self.rect.left = 55
        if self.rect.right > 345:
            self.rect.right = 345


# -----------------------------
# ENEMY CLASS
# -----------------------------
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 40
        self.height = 70
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.draw_car(self.image, RED)
        self.rect = self.image.get_rect()
        self.reset_position()

    def draw_car(self, surface, color):
        """Draw enemy car."""
        pygame.draw.rect(surface, color, (5, 10, 30, 50), border_radius=8)
        pygame.draw.rect(surface, BLACK, (10, 15, 20, 15), border_radius=4)

        # Wheels
        pygame.draw.circle(surface, BLACK, (8, 18), 5)
        pygame.draw.circle(surface, BLACK, (32, 18), 5)
        pygame.draw.circle(surface, BLACK, (8, 52), 5)
        pygame.draw.circle(surface, BLACK, (32, 52), 5)

    def reset_position(self):
        """Respawn enemy above the screen in random lane area."""
        self.rect.center = (random.randint(80, 320), -80)

    def move(self):
        """Move enemy downward."""
        global score
        self.rect.move_ip(0, SPEED)

        if self.rect.top > SCREEN_HEIGHT:
            score += 1
            self.reset_position()


# -----------------------------
# COIN CLASS
# -----------------------------
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = 24
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.draw_coin(self.image)
        self.rect = self.image.get_rect()
        self.spawn()

    def draw_coin(self, surface):
        """Draw a simple coin."""
        pygame.draw.circle(surface, YELLOW, (12, 12), 12)
        pygame.draw.circle(surface, BLACK, (12, 12), 12, 2)
        pygame.draw.circle(surface, (255, 235, 120), (12, 12), 7)

    def spawn(self):
        """Spawn coin at random position above the screen."""
        self.rect.center = (random.randint(80, 320), -30)

    def move(self):
        """Move coin downward."""
        self.rect.move_ip(0, SPEED)

        if self.rect.top > SCREEN_HEIGHT:
            self.spawn()


# -----------------------------
# CREATE OBJECTS
# -----------------------------
road = Road()
player = Player()
enemy = Enemy()
coin = Coin()

enemies = pygame.sprite.Group()
enemies.add(enemy)

coins = pygame.sprite.Group()
coins.add(coin)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemy)
all_sprites.add(coin)

# -----------------------------
# MAIN GAME LOOP
# -----------------------------
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Update objects
    road.update()
    player.move()
    enemy.move()
    coin.move()

    # Check if player collected a coin
    if pygame.sprite.spritecollideany(player, coins):
        coins_collected += 1
        coin.spawn()

    # Check collision with enemy
    if pygame.sprite.spritecollideany(player, enemies):
        road.draw(screen)

        for entity in all_sprites:
            screen.blit(entity.image, entity.rect)

        game_over_text = font_big.render("Game Over", True, BLACK)
        screen.blit(
            game_over_text,
            (
                SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2
            )
        )

        pygame.display.update()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()

    # Draw everything
    road.draw(screen)

    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)

    # Draw score on top left
    score_text = font_small.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Draw coins collected on top right
    coin_text = font_small.render(f"Coins: {coins_collected}", True, WHITE)
    screen.blit(coin_text, (SCREEN_WIDTH - coin_text.get_width() - 10, 10))

    pygame.display.update()
    clock.tick(FPS)
    