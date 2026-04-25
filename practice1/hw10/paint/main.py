import pygame
import sys

def main():
    pygame.init()

    WIDTH, HEIGHT = 900, 600
    TOOLBAR_HEIGHT = 80
    CANVAS_Y = TOOLBAR_HEIGHT

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Paint App")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Verdana", 20)
    small_font = pygame.font.SysFont("Verdana", 16)

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (220, 220, 220)
    DARK_GRAY = (80, 80, 80)
    RED = (255, 0, 0)
    GREEN = (0, 180, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    PURPLE = (160, 32, 240)
    ORANGE = (255, 140, 0)

    colors = [BLACK, RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE]
    color_rects = []

    for i, color in enumerate(colors):
        rect = pygame.Rect(20 + i * 50, 20, 35, 35)
        color_rects.append((rect, color))

    canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
    canvas.fill(WHITE)

    current_color = BLACK
    brush_size = 8
    tool = "brush"

    drawing = False
    last_pos = None
    start_pos = None
    preview_pos = None

    def draw_toolbar():
        pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))

        title = font.render("Tools: B-Brush  R-Rectangle  O-Circle  E-Eraser  C-Clear", True, BLACK)
        size_text = font.render(f"Size: {brush_size}", True, BLACK)
        tool_text = font.render(f"Current tool: {tool}", True, BLACK)

        screen.blit(title, (20, 55))
        screen.blit(size_text, (650, 15))
        screen.blit(tool_text, (650, 40))

        for rect, color in color_rects:
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)

            if color == current_color and tool != "eraser":
                pygame.draw.rect(screen, DARK_GRAY, rect.inflate(6, 6), 3)

        if tool == "eraser":
            eraser_text = small_font.render("Eraser", True, BLACK)
            screen.blit(eraser_text, (380, 25))

    def draw_line(surface, color, start, end, radius):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        steps = max(abs(dx), abs(dy))

        if steps == 0:
            pygame.draw.circle(surface, color, start, radius)
            return

        for i in range(steps + 1):
            x = int(start[0] + dx * i / steps)
            y = int(start[1] + dy * i / steps)
            pygame.draw.circle(surface, color, (x, y), radius)

    def normalize_rect(start, end):
        x1, y1 = start
        x2, y2 = end
        left = min(x1, x2)
        top = min(y1, y2)
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        return pygame.Rect(left, top, width, height)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_b:
                    tool = "brush"
                elif event.key == pygame.K_r:
                    tool = "rectangle"
                elif event.key == pygame.K_o:
                    tool = "circle"
                elif event.key == pygame.K_e:
                    tool = "eraser"
                elif event.key == pygame.K_c:
                    canvas.fill(WHITE)
                elif event.key == pygame.K_LEFTBRACKET:
                    brush_size = max(1, brush_size - 1)
                elif event.key == pygame.K_RIGHTBRACKET:
                    brush_size = min(50, brush_size + 1)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                # Color selection
                if my < TOOLBAR_HEIGHT:
                    for rect, color in color_rects:
                        if rect.collidepoint(event.pos):
                            current_color = color
                            if tool == "eraser":
                                tool = "brush"
                    continue

                # Start drawing on canvas
                if my >= TOOLBAR_HEIGHT:
                    drawing = True
                    start_pos = (mx, my - TOOLBAR_HEIGHT)
                    preview_pos = start_pos
                    last_pos = start_pos

                    if tool == "brush":
                        draw_line(canvas, current_color, start_pos, start_pos, brush_size)
                    elif tool == "eraser":
                        draw_line(canvas, WHITE, start_pos, start_pos, brush_size)

            if event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    mx, my = event.pos
                    end_pos = (mx, my - TOOLBAR_HEIGHT)

                    if tool == "rectangle":
                        rect = normalize_rect(start_pos, end_pos)
                        pygame.draw.rect(canvas, current_color, rect, 2)
                    elif tool == "circle":
                        center_x = (start_pos[0] + end_pos[0]) // 2
                        center_y = (start_pos[1] + end_pos[1]) // 2
                        radius = max(abs(end_pos[0] - start_pos[0]) // 2,
                                     abs(end_pos[1] - start_pos[1]) // 2)
                        pygame.draw.circle(canvas, current_color, (center_x, center_y), radius, 2)

                drawing = False
                last_pos = None
                start_pos = None
                preview_pos = None

            if event.type == pygame.MOUSEMOTION and drawing:
                mx, my = event.pos
                current_pos = (mx, my - TOOLBAR_HEIGHT)

                if tool == "brush":
                    draw_line(canvas, current_color, last_pos, current_pos, brush_size)
                    last_pos = current_pos
                elif tool == "eraser":
                    draw_line(canvas, WHITE, last_pos, current_pos, brush_size)
                    last_pos = current_pos
                elif tool in ("rectangle", "circle"):
                    preview_pos = current_pos

        screen.fill(WHITE)
        draw_toolbar()
        screen.blit(canvas, (0, TOOLBAR_HEIGHT))

        # Preview for rectangle or circle while dragging
        if drawing and tool in ("rectangle", "circle") and start_pos and preview_pos:
            preview_surface = canvas.copy()

            if tool == "rectangle":
                rect = normalize_rect(start_pos, preview_pos)
                pygame.draw.rect(preview_surface, current_color, rect, 2)
            elif tool == "circle":
                center_x = (start_pos[0] + preview_pos[0]) // 2
                center_y = (start_pos[1] + preview_pos[1]) // 2
                radius = max(abs(preview_pos[0] - start_pos[0]) // 2,
                             abs(preview_pos[1] - start_pos[1]) // 2)
                pygame.draw.circle(preview_surface, current_color, (center_x, center_y), radius, 2)

            screen.blit(preview_surface, (0, TOOLBAR_HEIGHT))

        pygame.display.flip()
        clock.tick(60)

main()