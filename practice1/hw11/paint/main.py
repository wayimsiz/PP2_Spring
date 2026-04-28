import pygame
import sys
import math

def main():
    pygame.init()

    WIDTH, HEIGHT = 900, 600
    TOOLBAR_HEIGHT = 100
    CANVAS_Y = TOOLBAR_HEIGHT

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Paint App with Shapes")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Verdana", 18)
    small_font = pygame.font.SysFont("Verdana", 15)

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
        """Draw toolbar with tools, colors, and current settings."""
        pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))

        title1 = font.render(
            "Tools: B-Brush  E-Eraser  R-Rectangle  O-Circle  S-Square  T-Right Triangle",
            True,
            BLACK
        )
        title2 = font.render(
            "Q-Equilateral Triangle  H-Rhombus  C-Clear  [ ] Brush size",
            True,
            BLACK
        )

        size_text = small_font.render(f"Size: {brush_size}", True, BLACK)
        tool_text = small_font.render(f"Current tool: {tool}", True, BLACK)

        screen.blit(title1, (20, 60))
        screen.blit(title2, (20, 80))
        screen.blit(size_text, (650, 15))
        screen.blit(tool_text, (650, 40))

        # Draw color buttons
        for rect, color in color_rects:
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)

            if color == current_color and tool != "eraser":
                pygame.draw.rect(screen, DARK_GRAY, rect.inflate(6, 6), 3)

        if tool == "eraser":
            eraser_text = small_font.render("Eraser selected", True, BLACK)
            screen.blit(eraser_text, (380, 25))

    def draw_line(surface, color, start, end, radius):
        """Draw smooth brush/eraser line."""
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
        """Create rectangle from any drag direction."""
        x1, y1 = start
        x2, y2 = end
        left = min(x1, x2)
        top = min(y1, y2)
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        return pygame.Rect(left, top, width, height)

    def normalize_square(start, end):
        """Create square from any drag direction."""
        x1, y1 = start
        x2, y2 = end

        size = min(abs(x2 - x1), abs(y2 - y1))

        left = x1 if x2 >= x1 else x1 - size
        top = y1 if y2 >= y1 else y1 - size

        return pygame.Rect(left, top, size, size)

    def right_triangle_points(start, end):
        """Return points for right triangle."""
        return [
            start,
            (start[0], end[1]),
            end
        ]

    def equilateral_triangle_points(start, end):
        """Return points for equilateral triangle."""
        x1, y1 = start
        x2, y2 = end

        side = x2 - x1

        if side == 0:
            side = 1

        height = abs(side) * math.sqrt(3) / 2

        p1 = (x1, y1)
        p2 = (x2, y1)

        # Triangle goes up if mouse is above start, otherwise down
        if y2 < y1:
            p3 = ((x1 + x2) // 2, y1 - height)
        else:
            p3 = ((x1 + x2) // 2, y1 + height)

        return [p1, p2, p3]

    def rhombus_points(start, end):
        """Return points for rhombus."""
        rect = normalize_rect(start, end)

        center_x = rect.centerx
        center_y = rect.centery

        return [
            (center_x, rect.top),
            (rect.right, center_y),
            (center_x, rect.bottom),
            (rect.left, center_y)
        ]

    def draw_shape(surface, selected_tool, start, end, color):
        """Draw selected shape on the surface."""
        if selected_tool == "rectangle":
            pygame.draw.rect(surface, color, normalize_rect(start, end), 2)

        elif selected_tool == "circle":
            center_x = (start[0] + end[0]) // 2
            center_y = (start[1] + end[1]) // 2
            radius = max(abs(end[0] - start[0]) // 2,
                         abs(end[1] - start[1]) // 2)
            pygame.draw.circle(surface, color, (center_x, center_y), radius, 2)

        elif selected_tool == "square":
            pygame.draw.rect(surface, color, normalize_square(start, end), 2)

        elif selected_tool == "right_triangle":
            pygame.draw.polygon(surface, color, right_triangle_points(start, end), 2)

        elif selected_tool == "equilateral_triangle":
            pygame.draw.polygon(surface, color, equilateral_triangle_points(start, end), 2)

        elif selected_tool == "rhombus":
            pygame.draw.polygon(surface, color, rhombus_points(start, end), 2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                # Tool selection
                elif event.key == pygame.K_b:
                    tool = "brush"
                elif event.key == pygame.K_e:
                    tool = "eraser"
                elif event.key == pygame.K_r:
                    tool = "rectangle"
                elif event.key == pygame.K_o:
                    tool = "circle"
                elif event.key == pygame.K_s:
                    tool = "square"
                elif event.key == pygame.K_t:
                    tool = "right_triangle"
                elif event.key == pygame.K_q:
                    tool = "equilateral_triangle"
                elif event.key == pygame.K_h:
                    tool = "rhombus"

                # Clear canvas
                elif event.key == pygame.K_c:
                    canvas.fill(WHITE)

                # Change brush size
                elif event.key == pygame.K_LEFTBRACKET:
                    brush_size = max(1, brush_size - 1)
                elif event.key == pygame.K_RIGHTBRACKET:
                    brush_size = min(50, brush_size + 1)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                # Color selection from toolbar
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

                    # Draw final shape after mouse release
                    if tool in (
                        "rectangle",
                        "circle",
                        "square",
                        "right_triangle",
                        "equilateral_triangle",
                        "rhombus"
                    ):
                        draw_shape(canvas, tool, start_pos, end_pos, current_color)

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

                elif tool in (
                    "rectangle",
                    "circle",
                    "square",
                    "right_triangle",
                    "equilateral_triangle",
                    "rhombus"
                ):
                    preview_pos = current_pos

        screen.fill(WHITE)
        draw_toolbar()
        screen.blit(canvas, (0, TOOLBAR_HEIGHT))

        # Preview selected shape while dragging
        if drawing and tool in (
            "rectangle",
            "circle",
            "square",
            "right_triangle",
            "equilateral_triangle",
            "rhombus"
        ) and start_pos and preview_pos:
            preview_surface = canvas.copy()
            draw_shape(preview_surface, tool, start_pos, preview_pos, current_color)
            screen.blit(preview_surface, (0, TOOLBAR_HEIGHT))

        pygame.display.flip()
        clock.tick(60)

main()