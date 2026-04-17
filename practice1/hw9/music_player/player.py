import pygame
import os

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        # Определяем путь к папке music относительно этого файла
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.music_dir = os.path.join(current_dir, "music")
        
        # Список твоих треков
        self.playlist = ["track1.mp3", "track2.mp3"]
        self.current_index = 0
        self.is_playing = False

    def play(self):
        # Проверяем наличие файлов перед загрузкой
        track_path = os.path.join(self.music_dir, self.playlist[self.current_index])
        
        if not os.path.exists(track_path):
            print(f"Ошибка: Файл {track_path} не найден!")
            return

        # Если музыка на паузе или остановлена — загружаем и играем
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(track_path)
            pygame.mixer.music.play()
        else:
            pygame.mixer.music.unpause()
            
        self.is_playing = True

    def stop(self):
        pygame.mixer.music.pause() # На Mac лучше использовать pause/unpause для стабильности
        self.is_playing = False

    def next_track(self):
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self._reload_and_play()

    def prev_track(self):
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self._reload_and_play()

    def _reload_and_play(self):
        track_path = os.path.join(self.music_dir, self.playlist[self.current_index])
        if os.path.exists(track_path):
            pygame.mixer.music.load(track_path)
            pygame.mixer.music.play()
            self.is_playing = True

    def get_current_track_name(self):
        return self.playlist[self.current_index]

    def get_pos_str(self):
        # Получаем время в секундах
        pos_ms = pygame.mixer.music.get_pos()
        if pos_ms == -1: return "00:00"
        seconds = int((pos_ms / 1000) % 60)
        minutes = int((pos_ms / (1000 * 60)) % 60)
        return f"{minutes:02d}:{seconds:02d}"