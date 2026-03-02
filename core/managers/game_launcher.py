import sys
import os

class GameLauncher:
    def __init__(self):
        self.original_cwd = os.getcwd()
        self.original_path = sys.path.copy()

    def start(self, game_data):
        game_class = game_data["class"]
        game_folder = str(game_data["root_path"]) 

        try:
            os.chdir(game_folder)
            
            if game_folder not in sys.path:
                sys.path.insert(0, game_folder)

            print(f" Iniciando instancia de: {game_data['title']}")
            
            try:
                return game_class()
            except TypeError:
                from enfocate import GameMetadata
                generic_meta = GameMetadata(
                    title=game_data.get("title", "Game"),
                    description=game_data.get("desc", "No description"),
                    authors=["Equipo Externo"],
                    group_number=1
                )
                return game_class(generic_meta)

        except Exception as e:
            print(f" Error crítico al instanciar: {e}")
            self.stop()
            return None
        
    def stop(self):
        modules_conflictivos = ['constantes', 'audio', 'menu', 'settings', 'config']

        for mod in modules_conflictivos:
            if mod in sys.modules:
                del sys.modules[mod]
                
        os.chdir(self.original_cwd)
        sys.path = self.original_path.copy()