import pygame
import json
import os
import sys
from pygame import mixer
from game.classes import Pokemon, HealthBar
from game.functions import *

# Initialize Pygame and Mixer
pygame.init()
mixer.init()

# Load sounds
title_music = mixer.Sound("sounds/Title_Screen.mp3")
battle_music = mixer.Sound("sounds/Battle3.mp3")
attack_sound = mixer.Sound("sounds/Cut.mp3")
victory_music = mixer.Sound("sounds/Victory.mp3")
battle_music.set_volume(0.5)
attack_sound.set_volume(1.0)

# Set up screen
screen_info = pygame.display.Info()
screen_width, screen_height = int(screen_info.current_w * 0.75), int(
    screen_info.current_h * 0.55
)
bottom_panel, screen_height_wpanel = int(screen_height * 0.35), screen_height + int(
    screen_height * 0.35
)
screen = pygame.display.set_mode((screen_width, screen_height_wpanel))
pygame.display.set_caption("Pokemon Battle")

# Colors and fonts
white, black, blue, red = (255, 255, 255), (0, 0, 0), (0, 0, 255), (255, 0, 0)
font, font2 = pygame.font.SysFont("Arial Bold", 56), pygame.font.SysFont(
    "Arial Bold", 100
)

# Load images
scaled_bg_img = pygame.transform.scale(
    pygame.image.load("img/bg/Untitled design.png"), (screen_width, screen_height)
)
title_image = pygame.transform.scale(
    pygame.image.load("img/pba_logo.png"), (screen_width // 3.5, screen_height // 3.5)
)
instructions_image = pygame.transform.scale(
    pygame.image.load("img/bg/instructions.png"), (screen_width, screen_height + 300)
)

# Load pokedex data
with open("pokedex.json", "r") as file:
    pokedex_data = json.load(file)

# Global variables
play_button_rect = instructions_button_rect = quit_button_rect = None
pokemons_per_row, rows_per_page, padding, rect_width, rect_height = 6, 3, 50, 250, 250
current_page = 0


def draw_message(screen, message, color, duration=2):
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < duration * 1000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(white)
        screen.blit(
            font2.render(message, True, color),
            (
                screen_width // 2 - font2.size(message)[0] // 2,
                screen_height // 2 - font2.size(message)[1] // 2,
            ),
        )
        pygame.display.flip()
        pygame.time.delay(50)


def draw_main_menu():
    global play_button_rect, instructions_button_rect, quit_button_rect
    screen.fill(white)
    screen.blit(
        title_image,
        (screen_width // 2 - title_image.get_width() // 2, screen_height // 8),
    )
    play_button_rect = pygame.Rect(
        screen_width // 2 - 180, screen_height // 1.5 - 30, 400, 90
    )
    instructions_button_rect = pygame.Rect(
        screen_width // 2 - 230, screen_height // 1.5 + 80, 500, 90
    )
    quit_button_rect = pygame.Rect(
        screen_width // 2 - 180, screen_height // 1.5 + 190, 400, 90
    )
    draw_button(screen, "Play Game", font2, play_button_rect, white, black, black)
    draw_button(
        screen, "Instructions", font2, instructions_button_rect, white, black, black
    )
    draw_button(screen, "Quit", font2, quit_button_rect, white, black, black)
    pygame.display.flip()


def main_menu():
    mixer.Sound.stop(battle_music)
    mixer.Sound.stop(victory_music)
    mixer.Sound.play(title_music, loops=-1)
    while True:
        draw_main_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    return "play"
                elif instructions_button_rect.collidepoint(event.pos):
                    return "instructions"
                elif quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


def draw_pokemon_selection(pokemon_list, selected_pokemon, title):
    screen.fill(white)
    screen.blit(
        font2.render(title, True, black),
        (screen_width // 2 - font2.size(title)[0] // 2, 50),
    )
    for index, pokemon in enumerate(
        pokemon_list[current_page * 18 : (current_page + 1) * 18]
    ):
        x, y = 300 + (index % 6) * (rect_width + padding), 200 + (index // 6) * (
            rect_height + padding + 50
        )
        pokemon_rect = pygame.Rect(x, y, rect_width, rect_height)
        pygame.draw.rect(
            screen, blue if selected_pokemon == pokemon else black, pokemon_rect, 2
        )
        img_path = (
            f'img/pokemons/{pokemon["pokemon_name"]}/{pokemon["pokemon_name"]}.png'
        )
        if os.path.isfile(img_path):
            screen.blit(
                pygame.transform.scale(
                    pygame.image.load(img_path), (rect_width + 80, rect_height + 80)
                ),
                (x - 40, y - 80),
            )
        screen.blit(
            font.render(pokemon["pokemon_name"], True, black),
            (
                x + rect_width // 2 - font.size(pokemon["pokemon_name"])[0] // 2,
                y + rect_height - font.size(pokemon["pokemon_name"])[1] // 2 + 30,
            ),
        )
    pygame.display.flip()


def pokemon_selection_screen():
    global current_page
    pokemon_list = pokedex_data["pokedex"]
    selected_pokemon, player = [None, None], 0
    while None in selected_pokemon:
        draw_pokemon_selection(
            pokemon_list, selected_pokemon[player], f"Player {player + 1}'s Pokemon"
        )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, pokemon in enumerate(pokemon_list):
                    x, y = 300 + (i % 6) * (rect_width + padding), 200 + (i // 6) * (
                        rect_height + padding
                    )
                    if pygame.Rect(x, y, rect_width, rect_height).collidepoint(
                        event.pos
                    ):
                        selected_pokemon[player], player = pokemon, player + 1
                        if player >= 2:
                            return selected_pokemon
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and (current_page + 1) * 18 < len(
                    pokemon_list
                ):
                    current_page += 1
                elif event.key == pygame.K_LEFT and current_page > 0:
                    current_page -= 1


def handle_attack_click(mouse_pos, attack_rects, attacker, defender):
    for i, rect in enumerate(attack_rects):
        if rect.collidepoint(mouse_pos):
            attack = attacker.attacks[i]
            defender.health -= attack["power"]
            if defender.health <= 0:
                defender.alive = False
                return attacker.name, attack["name"], attack["power"]
            return None, attack["name"], attack["power"]
    return None, None, None


def victory_screen(winner):
    mixer.Sound.stop(title_music)
    mixer.Sound.stop(battle_music)
    mixer.Sound.play(victory_music, loops=-1)
    while True:
        screen.fill(white)
        screen.blit(
            font2.render(f"{winner} Wins!", True, black),
            (
                screen_width // 2 - font2.size(f"{winner} Wins!")[0] // 2,
                screen_height // 4,
            ),
        )
        draw_button(
            screen,
            "Play Again",
            font2,
            pygame.Rect(screen_width // 2 - 200, screen_height // 2, 400, 100),
            white,
            black,
            black,
        )
        draw_button(
            screen,
            "Quit",
            font2,
            pygame.Rect(screen_width // 2 - 200, screen_height // 2 + 150, 400, 100),
            white,
            black,
            black,
        )
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(
                    screen_width // 2 - 200, screen_height // 2, 400, 100
                ).collidepoint(event.pos):
                    mixer.Sound.stop(victory_music)
                    return "play_again"
                elif pygame.Rect(
                    screen_width // 2 - 200, screen_height // 2 + 150, 400, 100
                ).collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


def instructions_screen():
    while True:
        screen.fill(white)
        screen.blit(instructions_image, (0, 0))
        draw_button(
            screen,
            "Back to Main Menu",
            font2,
            pygame.Rect(screen_width // 2 - 350, screen_height + 150, 700, 80),
            white,
            black,
            black,
        )
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mixer.Sound.stop(title_music)
                if pygame.Rect(
                    screen_width // 2 - 350, screen_height + 150, 700, 80
                ).collidepoint(event.pos):
                    return


def poke_battle(poke1, poke2):
    mixer.Sound.stop(title_music)
    mixer.Sound.stop(victory_music)
    mixer.Sound.play(battle_music)
    poke1_healthbar, poke2_healthbar = HealthBar(
        screen, 320, screen_height - 200, poke1.max_health
    ), HealthBar(screen, 1650, screen_height - 200, poke2.max_health)
    turn = 0
    winner = None
    while winner is None:
        show_bg(screen, scaled_bg_img)
        show_panel(screen, screen_height, screen_width, bottom_panel, white)
        poke1_healthbar.show_hp(screen, poke1, white, black, blue, red, show_info, font)
        poke2_healthbar.show_hp(screen, poke2, white, black, blue, red, show_info, font)
        poke1.show_flip(screen)
        poke2.show(screen)
        attack_rects = create_attack_rects(screen_height, screen_width)
        for i, rect in enumerate(attack_rects):
            pokemon = poke1 if i < 4 else poke2
            pygame.draw.rect(screen, blue if i < 4 else red, rect)
            render_text(screen, pokemon.attacks[i % 4]["name"], font, white, rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if turn == 0 and mouse_pos[0] < screen_width / 2:
                    winner, attack_name, _ = handle_attack_click(
                        mouse_pos, attack_rects[:4], poke1, poke2
                    )
                    poke2.start_blinking()
                    poke2.start_shaking()
                    turn = 1
                elif turn == 1 and mouse_pos[0] >= screen_width / 2:
                    winner, attack_name, _ = handle_attack_click(
                        mouse_pos, attack_rects[4:], poke2, poke1
                    )
                    poke1.start_blinking()
                    poke1.start_shaking()
                    turn = 0
                if winner:
                    return winner


if __name__ == "__main__":
    while True:
        choice = main_menu()
        if choice == "play":
            selected_pokemon = pokemon_selection_screen()
            poke1_data = next(
                pokemon
                for pokemon in pokedex_data["pokedex"]
                if pokemon["pokemon_name"] == selected_pokemon[0]["pokemon_name"]
            )
            poke2_data = next(
                pokemon
                for pokemon in pokedex_data["pokedex"]
                if pokemon["pokemon_name"] == selected_pokemon[1]["pokemon_name"]
            )
            poke1, poke2 = Pokemon(
                550,
                280,
                selected_pokemon[0]["pokemon_name"],
                100,
                poke1_data["attacks"],
            ), Pokemon(
                1850,
                280,
                selected_pokemon[1]["pokemon_name"],
                100,
                poke2_data["attacks"],
            )
            winner = poke_battle(poke1, poke2)
            if victory_screen(winner) != "play_again":
                break
        elif choice == "instructions":
            instructions_screen()
