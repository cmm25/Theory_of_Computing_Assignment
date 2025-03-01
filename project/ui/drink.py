import pygame 
import random
from constants import *
class Drink:
    def __init__(self, x, y, name, color, size=80):
            self.rect = pygame.Rect(x, y, size, size * 1.5)
            self.name = name
            self.color = color
            self.is_dispensed = False
            self.is_falling = False
            self.original_y = y
            self.original_x = x
            self.fall_speed = 0
            self.size = size
            self.rotation = 0
            self.rotation_speed = 0

    def draw(self, screen):
        if self.is_falling:
            # If falling, draw at current position with rotation
            rotated_surface = pygame.Surface(
                (self.size, self.size * 1.5), pygame.SRCALPHA)
            self.draw_can(rotated_surface)
            rotated = pygame.transform.rotate(rotated_surface, self.rotation)
            screen.blit(rotated, (self.rect.x - (rotated.get_width() - self.rect.width) // 2,
                                  self.rect.y - (rotated.get_height() - self.rect.height) // 2))
        

    def draw_can(self, surface):
        # Can body
        pygame.draw.rect(surface, self.color,
                            (0, 0, self.rect.width, self.rect.height),
                            border_radius=10)

        # Can top and bottom
        pygame.draw.ellipse(surface, DARK_GRAY,
                            (5, 5, self.rect.width - 10, 15))
        pygame.draw.ellipse(surface, DARK_GRAY,
                            (5, self.rect.height - 20, self.rect.width - 10, 15))

        # Label
        label_rect = pygame.Rect(10, self.rect.height // 4,
                                 self.rect.width - 20, self.rect.height // 2)
        pygame.draw.rect(surface, WHITE, label_rect, border_radius=5)

        # Drink name
        text_surf = FONT_BOLD.render(self.name[0], True, BLACK)
        text_rect = text_surf.get_rect(
            center=(self.rect.width // 2, self.rect.height // 2))
        surface.blit(text_surf, text_rect)

        # Reflection highlight
        highlight_surf = pygame.Surface(
            (10, self.rect.height - 30), pygame.SRCALPHA)
        for i in range(10):
            alpha = 100 - i * 10
            pygame.draw.line(highlight_surf, (255, 255, 255, alpha),
                                (i, 0), (i, self.rect.height - 30), 1)
        surface.blit(highlight_surf, (self.rect.width - 20, 15))

    def update(self):
        if self.is_dispensed and not self.is_falling:
            # Start fall animation after a short delay
            self.is_falling = True
            self.fall_speed = 2
            self.rotation_speed = random.uniform(-3, 3)

        if self.is_falling:
            # Update position
            self.fall_speed += 0.2
            self.rect.y += self.fall_speed

            # Update rotation
            self.rotation += self.rotation_speed

            # Reset if the drink falls off the screen
            if self.rect.y > SCREEN_HEIGHT:
                self.is_dispensed = False
                self.is_falling = False
                self.rect.y = self.original_y
                self.rect.x = self.original_x
                self.fall_speed = 0
                self.rotation = 0