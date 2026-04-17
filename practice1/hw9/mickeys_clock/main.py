import pygame
import sys
from clock import MickeyClock

def main():
    pygame.init()

    width, height = 800, 800
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Mickey Mouse Clock")

    app = MickeyClock(width, height)
    timer = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        app.render(screen)
        pygame.display.flip()
        timer.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()