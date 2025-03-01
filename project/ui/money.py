import pygame
import random
import math
from constants import *
class Coin:
    def __init__(self, x, y, value, size=70):
        self.rect = pygame.Rect(x, y, size, size)
        self.value = value
        self.dragging = False
        self.original_pos = (x, y)
        self.size = size
        self.shine_angle = random.uniform(0, 2 * math.pi)
        self.shine_speed = random.uniform(0.01, 0.03)

    def draw(self, screen):
        if self.value == 10:
            color = YELLOW
            border_color = (212, 172, 13)
            shine_color = (255, 236, 139, 150)
        elif self.value == 20:
            color = LIGHT_GRAY
            border_color = (150, 150, 150)
            shine_color = (220, 220, 220, 150)
        else:
            color = ORANGE
            border_color = (202, 111, 30)
            shine_color = (246, 185, 128, 150)

        # Draw coin body
        pygame.draw.circle(screen, border_color,
                           self.rect.center, self.rect.width // 2)
        pygame.draw.circle(screen, color, self.rect.center,
                           self.rect.width // 2 - 2)

        # Inner ring
        pygame.draw.circle(
            screen, border_color, self.rect.center, self.rect.width // 2 - 8, 2
        )

        # Dynamic shine effect
        self.shine_angle += self.shine_speed
        shine_pos = (
            self.rect.centerx +
            math.cos(self.shine_angle) * (self.rect.width // 4),
            self.rect.centery +
            math.sin(self.shine_angle) * (self.rect.width // 4),
        )
        shine_surf = pygame.Surface(
            (self.rect.width // 3, self.rect.width // 3), pygame.SRCALPHA
        )
        pygame.draw.circle(
            shine_surf,
            shine_color,
            (self.rect.width // 6, self.rect.width // 6),
            self.rect.width // 6,
        )
        screen.blit(
            shine_surf,
            (shine_pos[0] - self.rect.width // 6,
             shine_pos[1] - self.rect.width // 6),
        )

        text_surf = FONT_BOLD.render(f"{self.value}", True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

        if self.dragging:
            pygame.draw.circle(screen, WHITE, self.rect.center,
                               self.rect.width // 2, 2)

    def is_clicked(self, pos):
        # Check if the point is inside the circle
        distance = (
            (pos[0] - self.rect.centerx) ** 2 +
            (pos[1] - self.rect.centery) ** 2
        ) ** 0.5
        return distance <= self.rect.width // 2

    def update_pos(self, pos):
        if self.dragging:
            self.rect.centerx = pos[0]
            self.rect.centery = pos[1]

    def reset_position(self):
        self.rect.x, self.rect.y = self.original_pos
        self.dragging = False


class Note:
    def __init__(self, x, y, value, width=120, height=60):
        # Ensure height is never zero
        height = max(1, height)
        self.rect = pygame.Rect(x, y, width, height)
        self.value = value
        self.dragging = False
        self.original_pos = (x, y)
        self.width = width
        self.height = height
        self.shine_offset = random.randint(-10, 10)

    def draw(self, screen):
        "COLOR ARE IN SHADES SO SHADES OF GREEN THEN BLUE THEN RED ETC.."
        if self.value == 50:
            base_color = (200, 255, 200)
            accent_color = (46, 204, 113)
        elif self.value == 100:
            base_color = (173, 216, 230)
            accent_color = (41, 128, 185)
        elif self.value == 200:
            base_color = (255, 200, 200)
            accent_color = (231, 76, 60)
        elif self.value == 500:
            base_color = (230, 190, 230)
            accent_color = (142, 68, 173)
        else:
            base_color = (255, 255, 200)
            accent_color = (243, 156, 18)

        pygame.draw.rect(
            screen,
            accent_color,
            (self.rect.x, self.rect.y, self.rect.width, self.rect.height),
            border_radius=5,
        )

        inner_rect = pygame.Rect(
            self.rect.x + 2, self.rect.y + 2, self.rect.width - 4, self.rect.height - 4
        )
        pygame.draw.rect(screen, base_color, inner_rect, border_radius=5)

        pygame.draw.rect(
            screen,
            accent_color,
            (
                self.rect.x + 10,
                self.rect.y + 10,
                self.rect.width - 20,
                self.rect.height - 20,
            ),
            1,
            border_radius=3,
        )

        text_surf = FONT_BOLD.render(f"{self.value} Shs", True, DARK_GRAY)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

        # safety check
        if self.rect.height > 0:
            shine_y = (pygame.time.get_ticks() // 20 + self.shine_offset) % (
                self.rect.height * 2
            ) - self.rect.height
        else:
            shine_y = 0  # Fallback if height is zero

        shine_surf = pygame.Surface((self.rect.width, 10), pygame.SRCALPHA)
        for i in range(10):
            alpha = 255 - i * 25
            pygame.draw.line(
                shine_surf, (255, 255, 255, alpha), (0,i), (self.rect.width, i), 1)
        screen.blit(shine_surf, (self.rect.x, self.rect.y + shine_y))

        if self.dragging:
            pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=5)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def update_pos(self, pos):
        if self.dragging:
            self.rect.centerx = pos[0]
            self.rect.centery = pos[1]

    def reset_position(self):
        self.rect.x, self.rect.y = self.original_pos
        self.dragging = False
