# main.py
import pygame
import sys
from game import SnakeGame, WIDTH, HEIGHT, load_settings, save_settings
from db import init_db, get_top_scores, get_personal_best

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS4 Snake Game")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (220, 220, 220)
DARK_GRAY = (80, 80, 80)
RED = (220, 20, 60)
GREEN = (0, 200, 0)
BLUE = (0, 100, 255)

font = pygame.font.SysFont("Verdana", 20)
small_font = pygame.font.SysFont("Verdana", 16)
big_font = pygame.font.SysFont("Verdana", 44)

settings = load_settings()
username = "Player"


class Button:
    """Simple button for Pygame screens."""

    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self):
        mouse = pygame.mouse.get_pos()
        color = GRAY if not self.rect.collidepoint(mouse) else (190, 190, 190)

        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=10)

        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


def center_text(text, y, fnt=font, color=BLACK):
    """Draw centered text."""
    surface = fnt.render(text, True, color)
    rect = surface.get_rect(center=(WIDTH // 2, y))
    screen.blit(surface, rect)


def username_screen():
    """Ask username using keyboard in Pygame."""
    global username

    name = ""

    while True:
        screen.fill(WHITE)
        center_text("Enter Username", 160, big_font)
        center_text("Press Enter to continue", 380, small_font)

        input_box = pygame.Rect(130, 260, 340, 50)
        pygame.draw.rect(screen, GRAY, input_box)
        pygame.draw.rect(screen, BLACK, input_box, 2)

        text_surface = font.render(name + "|", True, BLACK)
        screen.blit(text_surface, (input_box.x + 10, input_box.y + 12))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    username = name.strip() if name.strip() else "Player"
                    return

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                elif event.key == pygame.K_ESCAPE:
                    username = "Player"
                    return

                else:
                    if event.unicode:
                        name += event.unicode

        pygame.display.update()
        clock.tick(60)


def main_menu():
    """Main menu screen."""
    buttons = [
        Button(200, 210, 200, 50, "Play"),
        Button(200, 280, 200, 50, "Leaderboard"),
        Button(200, 350, 200, 50, "Settings"),
        Button(200, 420, 200, 50, "Quit"),
    ]

    while True:
        screen.fill(WHITE)

        center_text("TSIS4 Snake", 120, big_font)

        for button in buttons:
            button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if buttons[0].clicked(event):
                username_screen()
                run_game()

            elif buttons[1].clicked(event):
                leaderboard_screen()

            elif buttons[2].clicked(event):
                settings_screen()

            elif buttons[3].clicked(event):
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)


def leaderboard_screen():
    """Show top 10 scores from PostgreSQL."""
    back_button = Button(200, 520, 200, 50, "Back")

    while True:
        screen.fill(WHITE)
        center_text("Leaderboard", 70, big_font)

        try:
            rows = get_top_scores()
        except Exception as e:
            rows = []
            center_text("Database error", 250, font, RED)
            center_text(str(e)[:45], 285, small_font, RED)

        if rows:
            header = small_font.render("Rank  Username      Score   Level   Date", True, BLACK)
            screen.blit(header, (45, 130))

            y = 165

            for index, row in enumerate(rows, start=1):
                username_row, score, level, date = row
                line = f"{index:<5} {username_row:<12} {score:<7} {level:<7} {date}"
                text = small_font.render(line, True, BLACK)
                screen.blit(text, (45, y))
                y += 32

        else:
            center_text("No scores yet", 250, font)

        back_button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if back_button.clicked(event):
                return

        pygame.display.update()
        clock.tick(60)


def settings_screen():
    """Settings screen: grid, sound, snake color."""
    global settings

    colors = [
        [0, 200, 0],
        [0, 100, 255],
        [220, 20, 60],
        [160, 32, 240],
        [255, 140, 0]
    ]

    buttons = [
        Button(170, 210, 260, 50, "Toggle Grid"),
        Button(170, 280, 260, 50, "Toggle Sound"),
        Button(170, 350, 260, 50, "Change Snake Color"),
        Button(170, 450, 260, 50, "Save & Back"),
    ]

    while True:
        screen.fill(WHITE)
        center_text("Settings", 100, big_font)

        grid_text = f"Grid: {'ON' if settings['grid_overlay'] else 'OFF'}"
        sound_text = f"Sound: {'ON' if settings['sound'] else 'OFF'}"
        color_text = f"Snake color: {settings['snake_color']}"

        screen.blit(font.render(grid_text, True, BLACK), (170, 170))
        screen.blit(font.render(sound_text, True, BLACK), (170, 240))
        screen.blit(font.render(color_text, True, BLACK), (170, 315))

        preview_color = tuple(settings["snake_color"])
        pygame.draw.rect(screen, preview_color, (440, 350, 40, 40))

        for button in buttons:
            button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if buttons[0].clicked(event):
                settings["grid_overlay"] = not settings["grid_overlay"]

            elif buttons[1].clicked(event):
                settings["sound"] = not settings["sound"]

            elif buttons[2].clicked(event):
                index = colors.index(settings["snake_color"]) if settings["snake_color"] in colors else 0
                settings["snake_color"] = colors[(index + 1) % len(colors)]

            elif buttons[3].clicked(event):
                save_settings(settings)
                return

        pygame.display.update()
        clock.tick(60)


def run_game():
    """Run the Snake game."""
    game = SnakeGame(screen, username, settings)

    while not game.game_over:
        clock.tick(game.current_speed())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                game.change_direction(event.key)

        game.update()
        game.draw()

        pygame.display.update()

    game_over_screen(game)


def game_over_screen(game):
    """Game over screen with final statistics."""
    retry_button = Button(200, 390, 200, 50, "Retry")
    menu_button = Button(200, 460, 200, 50, "Main Menu")

    best = max(game.personal_best, game.score)

    while True:
        screen.fill(WHITE)

        center_text("Game Over", 110, big_font, RED)
        center_text(f"Final Score: {game.score}", 210, font)
        center_text(f"Level Reached: {game.level}", 250, font)
        center_text(f"Personal Best: {best}", 290, font)

        retry_button.draw()
        menu_button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if retry_button.clicked(event):
                run_game()
                return

            elif menu_button.clicked(event):
                return

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    try:
        init_db()
    except Exception as e:
        print("Database initialization error:", e)

    main_menu()
