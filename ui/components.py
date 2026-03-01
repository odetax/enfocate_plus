import pygame

from core.settings import Settings

class GameCard:
    def __init__(self, title, description, cover):
        self.title = title
        self.description = description
        self.cover = cover
        self.card_box = pygame.Rect((0, 0), Settings.BOX_CARD_SIZE)

    def draw(self, surface, x, y, is_selected, cover_img=None):
        self.card_box.topleft = (x, y)

        if is_selected:
            offset = 30
            draw_rect = self.card_box.inflate(offset, offset)
            border_rect = draw_rect.inflate(12, 12)

            pygame.draw.rect(
                surface,
                Settings.COLORS["selected_color"],
                border_rect,
                width=6,
                border_radius=12
            )
        else:
            draw_rect = self.card_box

        if cover_img:
            if is_selected:
                cover_scaled = pygame.transform.smoothscale(cover_img, draw_rect.size)
                surface.blit(cover_scaled, draw_rect)
            else:
                surface.blit(cover_img, draw_rect)
        else:
            pygame.draw.rect(
                surface, 
                self.cover, 
                draw_rect, 
                border_radius=8
            )