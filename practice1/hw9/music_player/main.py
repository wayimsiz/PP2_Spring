import pygame
import sys
from player import MusicPlayer

def main():
    pygame.init()
    
    # Настройки окна
    screen = pygame.display.set_mode((500, 300))
    pygame.display.set_caption("Keyboard Music Player")
    
    # Цвета
    BG_COLOR = (25, 25, 25)
    TEXT_COLOR = (200, 200, 200)
    ACCENT_COLOR = (0, 200, 255)
    
    font = pygame.font.SysFont("Verdana", 20)
    info_font = pygame.font.SysFont("Verdana", 14)
    
    player = MusicPlayer()
    clock = pygame.time.Clock()

    while True:
        screen.fill(BG_COLOR)
        
        # 1. Обработка клавиш
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: # Play
                    player.play()
                elif event.key == pygame.K_s: # Stop (Pause)
                    player.stop()
                elif event.key == pygame.K_n: # Next
                    player.next_track()
                elif event.key == pygame.K_b: # Back
                    player.prev_track()
                elif event.key == pygame.K_q: # Quit
                    pygame.quit()
                    sys.exit()

        # 2. Отрисовка интерфейса
        # Название трека
        title_surf = font.render(f"Now Playing: {player.get_current_track_name()}", True, ACCENT_COLOR)
        screen.blit(title_surf, (50, 80))
        
        # Позиция времени
        time_surf = font.render(f"Time: {player.get_pos_str()}", True, TEXT_COLOR)
        screen.blit(time_surf, (50, 120))
        
        # Инструкция
        controls_text = [
            "P - Play | S - Stop",
            "N - Next | B - Back",
            "Q - Quit"
        ]
        
        for i, line in enumerate(controls_text):
            instr_surf = info_font.render(line, True, (100, 100, 100))
            screen.blit(instr_surf, (50, 200 + (i * 20)))

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()