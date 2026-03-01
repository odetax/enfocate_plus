import sys
import os
import importlib.util

from pathlib import Path
from enfocate import GameBase

class GameScanner:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parents[2]
        self.modules_dir = self.base_dir / "modules"

    def get_games_metadata(self):
        if not self.modules_dir.exists():
            return []

        directories = [d for d in self.modules_dir.iterdir() if d.is_dir()]
        GAMES_LIST = []
        original_sys_path = sys.path.copy()
        original_cwd = os.getcwd()

        for game_folder in directories:
            for m in list(sys.modules.keys()):
                if m.split('.')[0] in ["src", "config", "menu", "settings", "utils", "constantes", "audio", "instrucciones", "niveles", "tablero", "jugador", "game"]:
                    del sys.modules[m]

            filepath = None
            for name in ["main.py", "game.py", "juego.py"]:
                found = list(game_folder.rglob(name))
                if found:
                    filepath = found[0]
                    break
            
            if not filepath: continue

            try:
                game_dir = str(game_folder)
                code_dir = str(filepath.parent)
                os.chdir(game_dir)
                sys.path.insert(0, game_dir)
                if code_dir != game_dir: sys.path.insert(0, code_dir)

                module_name = f"loader_{game_folder.name.replace('-', '_')}"
                spec = importlib.util.spec_from_file_location(module_name, str(filepath))
                
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[module_name] = module
                    spec.loader.exec_module(module)
                    clase_juego = self._find_class_inheriting_from(module, GameBase)
                    
                    if clase_juego:
                        def crear_wrapper(metodo_real):
                            def compatible_update(inst, dt):
                                if hasattr(inst, 'estado_actual') and inst.estado_actual == "MENU":
                                    metodo_real(inst, dt)
                                elif hasattr(inst, 'run_preview') and metodo_real == GameBase.update:
                                    inst.run_preview()
                                    inst._stop_context()
                                else:
                                    metodo_real(inst, dt)
                            return compatible_update

                        clase_juego.update = crear_wrapper(clase_juego.update)

                        try:
                            instancia = clase_juego()
                            if not hasattr(instancia, 'metadata') or instancia.metadata is None:
                                from enfocate import GameMetadata
                                instancia.metadata = GameMetadata(
                                    title=game_folder.name, 
                                    description="Cargado vía modo compatibilidad", 
                                    authors=["Equipo Externo"], 
                                    group_number=1
                                )
                        except (TypeError, ValueError):
                            from enfocate import GameMetadata
                            mock_meta = GameMetadata(game_folder.name, "Revisar configuración", ["Sistema"], 1)
                            instancia = clase_juego(mock_meta)

                        if instancia:
                            cover_path = game_folder / "cover.png"
                            if not cover_path.exists():
                                cover_path = self.base_dir / "assets" / "images" / "default_cover.png"

                            GAMES_LIST.append({
                                "title": instancia.metadata.title,
                                "desc": instancia.metadata.description,
                                "color": (245, 245, 245),
                                "class": clase_juego,
                                "root_path": game_folder,
                                "cover_path": cover_path
                            })
                            print(f"✅ ¡CARGADO!: {instancia.metadata.title}")

            except Exception as e:
                print(f"❌ Error en {game_folder.name}: {e}")
            finally:
                sys.path = original_sys_path.copy()
                os.chdir(original_cwd)

        return GAMES_LIST

    def _find_class_inheriting_from(self, module, base_class):
        for name, obj in vars(module).items():
            if isinstance(obj, type):
                try:
                    if issubclass(obj, base_class) and obj is not base_class:
                        return obj
                except TypeError: pass
                if obj.__name__ in ["MiJuego", "Game"]:
                    if any(base.__name__ == "GameBase" for base in obj.__bases__):
                        return obj
        return None