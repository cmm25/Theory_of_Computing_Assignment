import pygame 
from project.constants import ( MONEY_SLOT_COLOR, 
    LIGHT_BLUE, FONT_BOLD,
    BLACK, DARK_GRAY,
    COIN_RETURN_COLOR,WHITE)

class MoneySlot:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.active = False
        self.active_time = 0

    def draw(self, screen):
        # Draw slot with 3D effect
        pygame.draw.rect(screen, BLACK,
                            (self.rect.x - 2, self.rect.y - 2,
                            self.rect.width + 4, self.rect.height + 4),
                            border_radius=5)

        slot_color = LIGHT_BLUE if self.active else MONEY_SLOT_COLOR
        pygame.draw.rect(screen, slot_color, self.rect, border_radius=5)

        # Darker inset to create depth
        inset_rect = pygame.Rect(self.rect.x + 5, self.rect.y + 5,
                                    self.rect.width - 10, self.rect.height - 10)
        pygame.draw.rect(screen, DARK_GRAY, inset_rect, border_radius=3)

        # Text
        text_surf = FONT_BOLD.render("INSERT MONEY", True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

        # Animation effect when active
        if self.active:
            current_time = pygame.time.get_ticks()
            if current_time - self.active_time < 500:  # 500ms animation
                progress = (current_time - self.active_time) / 500
                flash_alpha = int(255 * (1 - progress))
                flash_surface = pygame.Surface(
                    (self.rect.width, self.rect.height), pygame.SRCALPHA)
                flash_surface.fill((255, 255, 255, flash_alpha))
                screen.blit(flash_surface, self.rect)

    def activate(self):
        self.active = True
        self.active_time = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()
        if self.active and current_time - self.active_time > 500:
            self.active = False


class ChangeDisplay:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.coins = []
        self.notes = []
        self.animation_start = 0
        self.title = "Change Return"

    def add_change(self, denominations):
        self.coins = []
        self.notes = []
        self.animation_start = pygame.time.get_ticks()

        # Layout positions for returned money
        x_offset = self.rect.x + 20
        y_offset_coins = self.rect.y + 60
        y_offset_notes = self.rect.y + 140

        for denom in denominations:
            if denom <= 40:  # Coins
                coin = Coin(x_offset, y_offset_coins, denom, 60)
                self.coins.append(coin)
                x_offset += 70
                if x_offset > self.rect.right - 70:
                    x_offset = self.rect.x + 20
                    y_offset_coins += 70
            else:  # Notes
                note = Note(x_offset, y_offset_notes, denom, 100, 50)
                self.notes.append(note)
                x_offset += 110
                if x_offset > self.rect.right - 110:
                    x_offset = self.rect.x + 20
                    y_offset_notes += 60

    def draw(self, screen):
        # Draw change tray with a 3D effect
        pygame.draw.rect(screen, DARK_GRAY,
                         (self.rect.x - 5, self.rect.y - 5,
                          self.rect.width + 10, self.rect.height + 10),
                         border_radius=15)
        pygame.draw.rect(screen, COIN_RETURN_COLOR,
                         self.rect, border_radius=15)

        # Title text
        text_surf = FONT_BOLD.render(self.title, True, DARK_GRAY)
        text_rect = text_surf.get_rect(
            midtop=(self.rect.centerx, self.rect.y + 10))
        screen.blit(text_surf, text_rect)

        # Animation for newly returned change
        time_diff = pygame.time.get_ticks() - self.animation_start
        if time_diff < 1000:  # 1 second animation
            scale = min(1.0, time_diff / 1000)
            for coin in self.coins:
                coin_center = coin.rect.center
                coin.rect.width = coin.rect.height = int(coin.size * scale)
                coin.rect.center = coin_center
            for note in self.notes:
                note_center = note.rect.center
                note.rect.width = int(note.width * scale)
                note.rect.height = int(note.height * scale)
                note.rect.center = note_center

        # Draw coins and notes
        for coin in self.coins:
            coin.draw(screen)

        for note in self.notes:
            note.draw(screen)
