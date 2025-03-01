import pygame as game
from constants import *


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color,
                    text_color=BLACK, border_radius=10, font=FONT_BOLD):
        self.rect = game.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = font
        self.border_radius = border_radius
        self.is_hover = False
        self.is_active = True
        self.shadow_offset = 4

    def draw(self, screen):
        shadow_rect = self.rect.copy()
        shadow_rect.y += self.shadow_offset
        game.draw.rect(screen, (0, 0, 0, 128), shadow_rect,
                        border_radius=self.border_radius)

        color = self.hover_color if self.is_hover and self.is_active else self.color
        if not self.is_active:
            color = tuple(max(0, c - 70) for c in self.color)

        game.draw.rect(screen, color, self.rect,
                        border_radius=self.border_radius)
        game.draw.rect(screen, DARK_GRAY, self.rect, 2,
                        border_radius=self.border_radius)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

    def check_click(self, pos):
        return self.rect.collidepoint(pos)

    def set_active(self, active):
        self.is_active = active
    def set_text_color(self, color):
        self.text_color = color
