import pygame
import sys
import random
import math
from pygame.locals import *

from constants import *
from ui.button import Button
from ui.money import Coin, Note
from ui.display import ChangeDisplay, MoneySlot
from ui.drink import Drink
from core.vending import VendingMachine


def main():
    # Initialize pygame
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("JKUAT Soft Drink Vending Machine")
    clock = pygame.time.Clock()

    machine = VendingMachine()

    dispense_button = Button(650, 235, 150, 60, "DISPENSE", GREEN, LIGHT_GREEN, WHITE)
    cancel_button = Button(650, 310, 150, 60, "CANCEL", RED, LIGHT_RED, WHITE)

    quantity_buttons = []
    for i in range(5):
        quantity_buttons.append(
            Button(560 + i * 60, 410, 50, 50, str(i + 1), LIGHT_GRAY, WHITE, DARK_GRAY)
        )

    coins = [Coin(30, 560, 10), Coin(130, 560, 20), Coin(230, 560, 40)]

    notes = [
        Note(30, 690, 50),
        Note(160, 690, 100),
        Note(290, 690, 200),
        Note(420, 690, 500),
        Note(550, 690, 1000),
    ]

    drinks = []
    for i, (name, color) in enumerate(machine.drink_types):
        drinks.append(Drink(450 + i * 100, 130, name, color))

    money_slot = MoneySlot(635, 180, 180, 40)
    collect_change_button = Button(
        560,
        480,
        300,
        100,
        "COLLECT CHANGE",
        YELLOW,
        (255, 236, 139),
        BLACK,
        border_radius=15,
    )
    default_collect_text = "COLLECT CHANGE"

    # Main states
    dragging_item = None
    selected_quantity = 1

    pattern_rects = []
    for i in range(20):
        pattern_rects.append(
            {
                "rect": pygame.Rect(
                    random.randint(-100, SCREEN_WIDTH),
                    random.randint(-100, SCREEN_HEIGHT),
                    random.randint(50, 200),
                    random.randint(50, 200),
                ),
                "color": (
                    random.randint(235, 255),
                    random.randint(235, 255),
                    random.randint(235, 255),
                ),
                "speed": random.uniform(0.1, 0.3),
            }
        )

    # Main game
    running = True
    while running:

        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    for coin in coins:
                        if coin.is_clicked(mouse_pos):
                            coin.dragging = True
                            dragging_item = coin
                            break

                    if dragging_item is None:
                        for note in notes:
                            if note.is_clicked(mouse_pos):
                                note.dragging = True
                                dragging_item = note
                                break

                    # Check if dispense button was clicked
                    if (
                        dispense_button.check_click(mouse_pos)
                        and machine.state == "ready_to_dispense"
                    ):
                        machine.dispense_drink(selected_quantity)
                        for i in range(selected_quantity):
                            if i < len(drinks):
                                drinks[i].is_dispensed = True

                    # Check if cancel button was clicked
                    if cancel_button.check_click(mouse_pos):
                        machine.cancel_transaction()

                    for i, btn in enumerate(quantity_buttons):
                        if btn.check_click(mouse_pos) and btn.is_active:
                            selected_quantity = i + 1

                    # Check if collect change button was clicked
                    if (
                        collect_change_button.check_click(mouse_pos)
                        and machine.has_change_to_collect()
                    ):
                        machine.collect_change()
                        # Reset button text to default
                        collect_change_button.text = default_collect_text
                        # Update the message to confirm change collection
                        machine.message = "Change collected. Insert coins or notes for a new purchase."

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and dragging_item is not None:
                    # Check if item was dropped in the money slot
                    if money_slot.rect.collidepoint(mouse_pos):
                        if machine.insert_money(dragging_item.value):
                            money_slot.activate()

                    # Reset the item position
                    dragging_item.reset_position()
                    dragging_item = None

            elif event.type == pygame.MOUSEMOTION:
                # Update the position of the dragged item
                if dragging_item is not None:
                    dragging_item.update_pos(mouse_pos)

                # Check hover for buttons
                dispense_button.check_hover(mouse_pos)
                cancel_button.check_hover(mouse_pos)
                for btn in quantity_buttons:
                    btn.check_hover(mouse_pos)

        for drink in drinks:
            drink.update()

        money_slot.update()

        max_drinks = max(1, machine.current_amount // machine.drink_price)
        dispense_button.set_active(machine.state == "ready_to_dispense")

        for i, btn in enumerate(quantity_buttons):
            btn.set_active(i + 1 <= max_drinks and machine.state == "ready_to_dispense")

        if machine.state == "dispensing" or machine.state == "returning_money":
            machine.state = "waiting_for_collection"

        # Update pattern movement
        for pattern in pattern_rects:
            pattern["rect"].x += pattern["speed"]
            pattern["rect"].y += pattern["speed"]
            if pattern["rect"].x > SCREEN_WIDTH:
                pattern["rect"].x = -100
            if pattern["rect"].y > SCREEN_HEIGHT:
                pattern["rect"].y = -100

        # Draw background
        screen.fill((245, 245, 247))

        for pattern in pattern_rects:
            pygame.draw.rect(
                screen, pattern["color"], pattern["rect"], border_radius=20
            )

        # vending machine outline
        machine_rect = pygame.Rect(50, 50, 380, 450)
        shadow_rect = pygame.Rect(60, 60, 380, 450)
        pygame.draw.rect(screen, (0, 0, 0, 64), shadow_rect, border_radius=15)
        pygame.draw.rect(screen, MACHINE_COLOR, machine_rect, border_radius=15)
        pygame.draw.rect(screen, MACHINE_BORDER, machine_rect, 4, border_radius=15)

        title_shadow = FONT_LARGE.render("JKUAT Vending Machine", True, BLACK)
        title_text = FONT_LARGE.render("JKUAT Vending Machine", True, WHITE)
        screen.blit(title_shadow, (52, 22))
        screen.blit(title_text, (50, 20))

        # Draw LCD display
        lcd_rect = pygame.Rect(70, 70, 340, 40)
        pygame.draw.rect(screen, DISPLAY_BORDER, lcd_rect, border_radius=5)
        pygame.draw.rect(
            screen,
            DISPLAY_COLOR,
            (lcd_rect.x + 2, lcd_rect.y + 2, lcd_rect.width - 4, lcd_rect.height - 4),
            border_radius=5,
        )

        # Display amount
        amount_text = FONT_DISPLAY.render(
            f"Shs {machine.current_amount}", True, DISPLAY_TEXT_COLOR
        )
        screen.blit(amount_text, (lcd_rect.x + 10, lcd_rect.y + 10))

        # Message display
        message_rect = pygame.Rect(70, 120, 340, 30)
        pygame.draw.rect(screen, LIGHT_GRAY, message_rect, border_radius=5)
        message_text = FONT_REGULAR.render(machine.message, True, BLACK)
        # Truncate message if too long
        if message_text.get_width() > message_rect.width - 20:
            message_text = FONT_REGULAR.render(
                machine.message[:30] + "...", True, BLACK
            )
        screen.blit(message_text, (message_rect.x + 10, message_rect.y + 7))

        drink_window = pygame.Rect(70, 160, 340, 320)
        pygame.draw.rect(screen, (200, 200, 200, 128), drink_window, border_radius=10)
        pygame.draw.rect(screen, BLACK, drink_window, 2, border_radius=10)

        "drawing methods"
        for drink in drinks:
            drink.draw(screen)

        money_slot.draw(screen)
        collect_change_button.draw(screen)
        dispense_button.draw(screen)
        cancel_button.draw(screen)
        quantity_text = FONT_BOLD.render("Select quantity:", True, BLACK)
        screen.blit(quantity_text, (560, 380))
        for i, btn in enumerate(quantity_buttons):
            # Determine if this button is the selected quantity
            is_selected = (i + 1) == selected_quantity

            # Set appropriate colors based on selection state and if button is active
            if btn.is_active:
                if is_selected:
                    btn.color = BLUE
                    btn.hover_color = LIGHT_BLUE
                    btn.text_color = WHITE
                else:
                    btn.color = LIGHT_GRAY
                    btn.hover_color = WHITE
                    btn.text_color = DARK_GRAY
            else:
                # Inactive buttons
                btn.color = DARK_GRAY
                btn.hover_color = DARK_GRAY
                btn.text_color = LIGHT_GRAY

            btn.draw(screen)

        coin_text = FONT_BOLD.render("Available coins:", True, BLACK)
        screen.blit(coin_text, (30, 520))

        note_text = FONT_BOLD.render("Available notes:", True, BLACK)
        screen.blit(note_text, (30, 650))
        for coin in coins:
            coin.draw(screen)

        for note in notes:
            note.draw(screen)

        # Draw instructions
        instructions = [
            "1. Drag coins or notes to the INSERT MONEY slot",
            "2. When you have enough money, press DISPENSE",
            "3. Select how many drinks you want with the number buttons",
            "4. Collect your drinks and change",
        ]

        instruction_box = pygame.Rect(470, 50, 500, 120)
        pygame.draw.rect(
            screen, (255, 255, 255, 200), instruction_box, border_radius=10
        )
        pygame.draw.rect(screen, DARK_GRAY, instruction_box, 2, border_radius=10)

        instruction_title = FONT_BOLD.render("Instructions:", True, BLACK)
        screen.blit(instruction_title, (instruction_box.x + 10, instruction_box.y + 10))

        for i, instruction in enumerate(instructions):
            text = FONT_REGULAR.render(instruction, True, BLACK)
            screen.blit(text, (instruction_box.x + 15, instruction_box.y + 35 + i * 20))

        if dragging_item is not None:
            dragging_item.draw(screen)

        # Draw collect change button
        if machine.has_change_to_collect():
            collect_change_button.text = (
                f"{default_collect_text}: {machine.change_amount} Shs"
            )
            collect_change_button.set_active(True)
            collect_change_button.draw(screen)
        else:
            # Reset button text to default even when not displayed
            collect_change_button.text = default_collect_text
            collect_change_button.set_active(False)

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
