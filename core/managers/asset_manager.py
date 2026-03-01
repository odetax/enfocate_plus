from pathlib import Path

import pygame

from core.settings import Settings

class AssetManager:
    @staticmethod
    def load_all_assets():
        for name, file in Settings.IMAGES_MAP.items():
            if file is not None:
                path = Settings.IMAGES_PATH / file
                print(f"Intentando cargar imagen: {name} desde {path.absolute()}")
                
                if path.exists():
                    Settings.IMAGES[name] = pygame.image.load(str(path)).convert_alpha()
                    print(f"Éxito: {name}")
                else:
                    print(f"Error: Archivo no encontrado en {path}")
            else:
                print(f"Aviso: '{name}' en IMAGES_MAP es None")

        if hasattr(Settings, 'SOUNDS_MAP'):
            for name, file in Settings.SOUNDS_MAP.items():
                if file is not None:
                    path = Settings.SOUNDS_PATH / file
                    if path.exists():
                        Settings.SOUNDS[name] = pygame.mixer.Sound(str(path))
                    else:
                        print(f"Sonido no encontrado: {path}")

        for name, file in Settings.FONTS_MAP.items():
            if file is not None:
                path = Settings.FONTS_PATH / file
                if path.exists():
                    Settings.FONTS[name] = str(path)
                    print(f"Fuente registrada: {name}")
                else:
                    print(f"Fuente no encontrada: {path}")

    @staticmethod
    def load_game_covers(games_list):
        Settings.GAME_COVERS = {}
        
        for game in games_list:
            title = game["title"]
            print(f"DEBUG: Intentando asignar carátula para: '{title}'")
            
            if title in Settings.MANUAL_COVERS_MAP:
                filename = Settings.MANUAL_COVERS_MAP[title]
                path = Settings.IMAGES_PATH / filename
            else:
                path = Path(game["cover_path"])

            try:
                if not path.exists():
                    print(f"⚠️ No se encontró {path.name}, usando default_cover.png")
                    path = Settings.IMAGES_PATH / "default_cover.png"

                if path.exists():
                    surf = pygame.image.load(str(path)).convert_alpha()
                    surf = pygame.transform.smoothscale(surf, Settings.BOX_CARD_SIZE)
                    Settings.GAME_COVERS[title] = surf
                    print(f"✅ Carátula cargada para {title}")
                else:
                    raise FileNotFoundError
                    
            except Exception as e:
                print(f"❌ Error crítico en {title}: {e}")
                fallback = pygame.Surface(Settings.BOX_CARD_SIZE)
                fallback.fill((60, 60, 60))
                font = pygame.font.SysFont("Arial", 20)
                txt = font.render(title[:15], True, (200, 200, 200))
                fallback.blit(txt, (10, 10))
                Settings.GAME_COVERS[title] = fallback

    @staticmethod
    def get_image(key):
        return Settings.IMAGES.get(key)

    @staticmethod
    def get_font(key):
        return Settings.FONTS.get(key)