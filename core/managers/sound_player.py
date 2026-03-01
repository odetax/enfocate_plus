from pygame import mixer

from core.settings import Settings

class SoundPlayer:
    @staticmethod
    def play_music(music):
        path = Settings.SOUNDS_PATH / Settings.SOUNDS_MAP[music]
        mixer.music.load(str(path))
        mixer.music.play(-1)

    @staticmethod
    def play_sfx(key, volume=0.5):
        sound = Settings.SOUNDS.get(key)
        if sound:
            sound.set_volume(volume)
            sound.play()
        else:
            raise Exception(f"Error: El sonido {key} no existe en Settings.")

    @staticmethod
    def stop_all():
        mixer.music.stop()
        mixer.stop()
        print("Audio del sistema detenido.")