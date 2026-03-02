import sys
import pygame
from core.managers.sound_player import SoundPlayer
from core.settings import Settings
from core.managers.asset_manager import AssetManager
from ui.base import Screen
from ui.components import GameCard

class BootScreen(Screen):
    def __init__(self):
        self.image = AssetManager.get_image("bootsplash")
        self.alpha = 0
        self.timer = 0
        self.duration = 300
        
    def update(self, dt):
        self.timer += 1
        if self.alpha < 255:
            self.alpha = min(255, self.alpha + Settings.FADE_SPEED)
            if self.image:
                self.image.set_alpha(self.alpha)
        if self.timer >= self.duration:
            return "MAIN_MENU"
        return None

    def draw(self, surface):
        surface.fill((0, 0, 0))
        if self.image:
            surface.blit(self.image, (0, 0))

class MainMenu(Screen):
    def __init__(self, games_metadata):
        
        self.games = games_metadata
        self.cards = [
            GameCard(g["title"], g["desc"], g["color"]) 
            for g in self.games
        ]
        self.selected_index = 0
        self.scroll_x = 0
        self.target_scroll_x = 0
        self.font_title = pygame.font.Font(AssetManager.get_font("main_bold"), Settings.FONT_SIZE_TITLE)
        self.font_desc = pygame.font.Font(AssetManager.get_font("main_regular"), Settings.FONT_SIZE_DESC)
        SoundPlayer.play_music("menu")
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    SoundPlayer.play_sfx("moverse")
                    self.selected_index = min(len(self.cards) - 1, self.selected_index + 1)
                elif event.key == pygame.K_LEFT:
                    SoundPlayer.play_sfx("moverse")
                    self.selected_index = max(0, self.selected_index - 1)
                elif event.key == pygame.K_RETURN:
                    SoundPlayer.play_sfx("entrar")
                    self.pending_exit = {
                        "action": "LAUNCH",
                        "game_data": self.games[self.selected_index]
                    }
                    SoundPlayer.stop_all()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos
                    info_rect = pygame.Rect(0, 0, 40, 40)
                    info_rect.center = Settings.INFO_POS
                    exit_rect = pygame.Rect(0, 0, 40, 40)
                    exit_rect.center = Settings.EXIT_POS
                    if exit_rect.collidepoint(mouse_pos):
                        self.pending_exit = "QUIT"
                    elif info_rect.collidepoint(mouse_pos):
                        self.pending_exit = "INFO_SCREEN"

    def update(self, dt):
        item_full_width = Settings.BOX_CARD_SIZE[0] + Settings.SPACING
        self.target_scroll_x = -self.selected_index * item_full_width
        diff = self.target_scroll_x - self.scroll_x
        self.scroll_x += diff * Settings.SCROLL_SMOOTHING
        mouse_pos = pygame.mouse.get_pos()
        exit_rect = pygame.Rect(0, 0, 40, 40)
        exit_rect.center = Settings.EXIT_POS
        info_rect = pygame.Rect(0, 0, 40, 40)
        info_rect.center = Settings.INFO_POS
        if exit_rect.collidepoint(mouse_pos) or info_rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if hasattr(self, 'pending_exit'):
            state = self.pending_exit
            del self.pending_exit
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            return state 
        return None

    def draw(self, surface):
        surface.fill(Settings.COLORS["main_bg_color"])
        start_x = (Settings.S_WIDTH // 2) - (Settings.BOX_CARD_SIZE[0] // 2)
        for i, card in enumerate(self.cards):
            x_pos = start_x + (i * (Settings.BOX_CARD_SIZE[0] + Settings.SPACING)) + self.scroll_x
            y_pos = Settings.CAROUSEL_Y
            is_selected = (i == self.selected_index)
            cover_img = Settings.GAME_COVERS.get(card.title)
            card.draw(surface, x_pos, y_pos, is_selected, cover_img)
            if is_selected:
                self._draw_dynamic_info(surface, x_pos, y_pos, card)
        self._draw_system_ui(surface)

    def _draw_dynamic_info(self, surface, x, y, card):
        center_x = x + Settings.BOX_CARD_SIZE[0] // 2
        title_surf = self.font_title.render(card.title, True, Settings.COLORS["primary_color"])
        title_rect = title_surf.get_rect(center=(center_x, y - 90)) 
        surface.blit(title_surf, title_rect)
        max_width = 400 
        line_spacing = 5
        words = card.description.split(' ')
        lines = []
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word])
            if self.font_desc.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        lines.append(' '.join(current_line))
        start_y = y + Settings.BOX_CARD_SIZE[1] + 60
        for i, line in enumerate(lines):
            line_surf = self.font_desc.render(line, True, Settings.COLORS["secondary_color"])
            line_rect = line_surf.get_rect(center=(center_x, start_y + i * (Settings.FONT_SIZE_DESC + line_spacing)))
            surface.blit(line_surf, line_rect)

    def _draw_system_ui(self, surface):
        logo_surf = AssetManager.get_image("logo")
        if logo_surf:
            surface.blit(logo_surf, Settings.LOGO_POS)
        info_icon = AssetManager.get_image("icon_info")
        # if info_icon:
        #      info_rect = info_icon.get_rect(center=Settings.INFO_POS)
        #      surface.blit(info_icon, info_rect)
        # else:
        #      pygame.draw.circle(surface, Settings.COLORS["secondary_color"], Settings.INFO_POS, 16)
        exit_icon = AssetManager.get_image("icon_power")
        if exit_icon:
            exit_rect = exit_icon.get_rect(center=Settings.EXIT_POS)
            surface.blit(exit_icon, exit_rect)
        else:
            pygame.draw.circle(surface, Settings.COLORS["secondary_color"], Settings.EXIT_POS, 16)