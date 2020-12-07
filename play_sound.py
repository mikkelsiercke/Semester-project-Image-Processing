import pygame

pygame.mixer.init()
distance_sound = pygame.mixer.Sound('husk_afstand.mp3')
channel = pygame.mixer.Channel(0)


class Sound:
    def run_once_sound(self, f):
        def wrapper(*args, **kwargs):
            if not wrapper.has_run:
                wrapper.has_run = True
                return f(*args, **kwargs)

        wrapper.has_run = False
        return wrapper

    def play_sound(self):
        if not channel.get_busy():
            channel.play(distance_sound, loops=0)
