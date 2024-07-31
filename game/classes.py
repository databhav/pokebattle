import pygame
from game.functions import show_info


class Pokemon:
    def __init__(self, x, y, name, health, attacks):
        self.name = name
        self.health = health
        self.attacks = attacks
        self.max_health = 100
        self.alive = True
        self.blinking = False
        self.shaking = False
        self.blink_count = 0
        self.shake_count = 0

        img = pygame.image.load(f"img/pokemons/{self.name}/{self.name}.png")
        img_flip = pygame.transform.flip(img, True, False)
        self.image = pygame.transform.scale(
            img, (img.get_width() * 3, img.get_height() * 3)
        )
        self.image_flip = pygame.transform.scale(
            img_flip, (img_flip.get_width() * 3, img_flip.get_height() * 3)
        )
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def show(self, screen):
        if self.blinking:
            # Blink effect: alternate visibility
            if self.blink_count % 10 < 5:  # 5 frames visible, 5 frames hidden
                self.draw_pokemon(screen)
            self.blink_count += 1
            if self.blink_count > 20:  # Blinking for 20 frames
                self.blinking = False
                self.blink_count = 0
        else:
            self.draw_pokemon(screen)

        if self.shaking:
            # Shake effect: move sprite slightly
            shake_amount = 5 if self.shake_count % 10 < 5 else -5
            self.rect.centerx += shake_amount
            self.shake_count += 1
            if self.shake_count > 20:  # Shaking for 20 frames
                self.shaking = False
                self.shake_count = 0
        else:
            screen.blit(self.image, self.rect)

    def show_flip(self, screen):
        if self.blinking:
            if self.blink_count % 10 < 5:  # 5 frames visible, 5 frames hidden
                self.draw_pokemon_flip(screen)
            self.blink_count += 1
            if self.blink_count > 20:  # Blinking for 20 frames
                self.blinking = False
                self.blink_count = 0
        else:
            self.draw_pokemon_flip(screen)

        if self.shaking:
            shake_amount = 5 if self.shake_count % 10 < 5 else -5
            self.rect.centerx += shake_amount
            self.shake_count += 1
            if self.shake_count > 20:  # Shaking for 20 frames
                self.shaking = False
                self.shake_count = 0
        else:
            screen.blit(self.image_flip, self.rect)

    def draw_pokemon(self, screen):
        screen.blit(self.image, self.rect)

    def draw_pokemon_flip(self, screen):
        screen.blit(self.image_flip, self.rect)

    def start_blinking(self):
        self.blinking = True
        self.blink_count = 0

    def start_shaking(self):
        self.shaking = True
        self.shake_count = 0


class HealthBar:
    def __init__(self, screen, x, y, max_hp):
        self.x = x
        self.y = y
        self.max_hp = max_hp

    def show_hp(
        self, screen, poke, color1, color2, hp_color, max_hp_color, show_info, font
    ):
        self.hp = poke.health
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, color1, (self.x - 10, self.y - 60, 420, 120))
        show_info(
            screen, f"{poke.name} HP: {self.hp}", font, color2, self.x + 8, self.y - 50
        )
        pygame.draw.rect(screen, max_hp_color, (self.x, self.y, 400, 40))
        pygame.draw.rect(screen, hp_color, (self.x, self.y, 400 * ratio, 40))
