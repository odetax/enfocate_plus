from pathlib import Path

try:
    from enfocate import SCREEN_SIZE, FPS
except:
    SCREEN_SIZE = (1280, 720)
    FPS = 60

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings:
    TITLE = "Enfócate+ Launcher"
    S_WIDTH, S_HEIGHT = SCREEN_SIZE
    FPS = FPS

    FADE_SPEED = 3

    LOGO_POS = (32, 32)
    INFO_POS = (32, 656)
    EXIT_POS = (1216, 656)

    SCROLL_SMOOTHING = 0.1
    CAROUSEL_Y = 232
    SPACING = 30
    BOX_CARD_SIZE = (256, 256)

    FONT_SIZE_TITLE = 50
    FONT_SIZE_DESC = 18

    # Gestión de Rutas (Pathlib)
    ASSETS_PATH = BASE_DIR / "assets"
    IMAGES_PATH = ASSETS_PATH / "images"
    FONTS_PATH = ASSETS_PATH / "fonts"
    SOUNDS_PATH = ASSETS_PATH / "sounds"

    # Mapas de Assets (Nombres de archivos)
    IMAGES_MAP = {
        "bootsplash": "bootsplash.png",
        "logo": "enfocate_logo.png",
        "icon_power": "power_icon.png",
        "icon_info": "info_icon.png"
    }

    FONTS_MAP = {
        "main_bold": "WorkSans-SemiBold.ttf",
        "main_regular": "WorkSans-Medium.ttf"
    }

    SOUNDS_MAP = {}

    # Contenedores de Objetos Pygame (Cargados por AssetManager)
    IMAGES = {}
    FONTS = {}
    SOUNDS = {}

    # Lista vacía de juegos llenada en el arranque
    GAMES = []
    GAME_COVERS = {}

    # Diccionario para las carátulas cargadas manualmente
    MANUAL_COVERS_MAP = {
        "Maze: Light-Trace": "grupo1.png",
        "Crash": "grupo2.png",
        "Encuentra las diferencias": "grupo3.png",
        "G04_Keep_The_Cadence": "grupo4.png",
        "Purely Placed": "grupo5.png",
        "Sokoban": "grupo6.png",
        "Osu! Legacy": "grupo7.png",
        "Color Fusion": "grupo8.png",
        "FLIP IT": "grupo9.png",
        "Pescar Al Salmón": "grupo10.png",
        "Pomodoro Tower Defence": "grupo11.png",
        "Disk Sort Puzzle": "grupo12.png"
    }

    COLORS = {
        "main_bg_color": (45, 45, 45),
        "primary_color": (255, 255, 255),
        "secondary_color": (212, 212, 212),
        "selected_color": (0, 200, 255)
    }