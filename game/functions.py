import pygame


# Adding text to the panel
def show_info(screen, text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


# Showing bg image into the app
def show_bg(screen, scaled_bg_img):
    screen.blit(scaled_bg_img, (0, 0))


# Showing panel
def show_panel(screen, screen_height, screen_width, bottom_panel, color):
    panel_rect = pygame.Rect(0, screen_height, screen_width, bottom_panel)
    pygame.draw.rect(screen, color, panel_rect)


# Create rectangles for the attacks
def create_attack_rects(screen_height, screen_width):
    rects = []
    attack_width = 700
    attack_height = 70
    spacing = 10

    # Rectangles for left side
    for i in range(4):
        x = spacing
        y = screen_height + spacing + i * (attack_height + spacing)
        rect = pygame.Rect(x, y, attack_width, attack_height)
        rects.append(rect)

    # Rectangles for right side
    for i in range(4):
        x = screen_width - attack_width - spacing
        y = screen_height + spacing + i * (attack_height + spacing)
        rect = pygame.Rect(x, y, attack_width, attack_height)
        rects.append(rect)

    return rects


# Render text inside rectangles
def render_text(screen, text, font, color, rect):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def handle_attack_click(mouse_pos, attack_rects, attacking_pokemon, defending_pokemon):
    for i, rect in enumerate(attack_rects):
        if rect.collidepoint(mouse_pos):
            attack_index = i % 4
            attack = attacking_pokemon.attacks[attack_index]
            defending_pokemon.health -= attack["power"]
            if defending_pokemon.health < 0:
                defending_pokemon.health = 0
            break


def draw_button(screen, text, font, rect, color1, color2, border_color):
    # Draw the filled rectangle for the button
    pygame.draw.rect(screen, color1, rect)

    # Draw the text on the button
    text_surf = font.render(text, True, color2)
    screen.blit(
        text_surf,
        (
            rect.x + (rect.width - text_surf.get_width()) // 2,
            rect.y + (rect.height - text_surf.get_height()) // 2,
        ),
    )

    # Draw the border around the button
    pygame.draw.rect(screen, border_color, rect, 2)  # 2 is the width of the border


def draw_message(screen, message, color, duration=2):
    start_time = pygame.time.get_ticks()
    font_message = pygame.font.SysFont("Arial Bold", 50)
    while pygame.time.get_ticks() - start_time < duration * 1000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        text_surf = font_message.render(message, True, color)
        screen.blit(
            text_surf,
            (
                screen_width // 2 - text_surf.get_width() // 2,
                screen_height // 2 - text_surf.get_height() // 2,
            ),
        )
        pygame.display.flip()
        pygame.time.delay(50)
