from engine import Engine
from core.managers.game_scanner import GameScanner

def main():
    try:
        scanner = GameScanner()
        found_games = scanner.get_games_metadata()

        launcher = Engine(found_games)
        launcher.run()
        
    except Exception as e:
        import traceback
        print(f"Error crítico: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()