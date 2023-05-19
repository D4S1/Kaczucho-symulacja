import pygame
from sys import exit
import numpy as np
from random import randint, randrange
from collections import Counter
import matplotlib.pyplot as plt

from duck import Duck
from food import Food
from button import Button


# === MENU ===
def display_score(screen, font, start_time, pause):
    current_time = int(pygame.time.get_ticks() / 1000) -start_time -pause
    score_surf = font.render(f'Time: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(menu_width//2, 50))
    screen.blit(score_surf, score_rect)


def frozen_time(screen, font, time):
    time_surf = font.render(f'Time: {time}', False, (64, 64, 64))
    time_rect = time_surf.get_rect(center=(menu_width // 2, 50))
    screen.blit(time_surf, time_rect)


def calculate_pause(start_time):
    return int(pygame.time.get_ticks() / 1000) - start_time


def display_bio_density(screen, font, bio_density):
    score_surf = font.render(f'Bio_density: {bio_density}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(menu_width//2, 150))
    screen.blit(score_surf, score_rect)


def display_population(screen, font, ducks):
    score_surf = font.render(f'Populacja: {len(ducks.sprites())}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(menu_width//2, 250))
    screen.blit(score_surf, score_rect)


# === HELPER FUNCTIONS ===

def collision_sprite(ducks, bugs, rows, colums):
    """
    Funkcja sprawdza kolizje pomiędzy obiektami (czyt. czy kaczka weszła na bug'a)
    Jeżeli tak, to zwiększy energie kaczki i usunie obiekt bug'a
    :param ducks:
    :param bugs:
    :return: None
    """
    for duck in ducks.sprites():
        target_exist = False
        for bug in bugs.sprites():
            if pygame.sprite.collide_rect(duck, bug):
                duck.eat()
                bug.kill()
            # print(f"{duck.target}")
            # print(f"{(bug.rect.y // 15, (bug.rect.x - menu_width)//15 )=}")
            if duck.target == ((bug.rect.y // 15) % rows, (bug.rect.x - menu_width)//15 % colums):
                target_exist = True
        if not target_exist:
            # print(f"zmiana targetu")
            duck.target = None


# === GRAPH ===

def draw_population_graph(ax, group):
    """
    Funkcja rysuje wykres.
    Promień koła odpowiada liczbie kaczek o danych atryburach.
    :param ax:
    :param group:
    :return:
    """
    ax.clear()
    if group:
        x = [duck.speed for duck in group]
        y = [duck.sense for duck in group]
        count = Counter(zip(x, y))
        size = [50 * count[(x1, y1)] for x1, y1 in zip(x, y)]
        ax.set(xlim=(0, 15), ylim=(0, 10), xlabel="speed", ylabel="sense", title="Populacja kaczek")
        ax.set_xlim(0, 15)
        ax.set_ylim(0, 10)
        ax.scatter(x, y, s=size)
    plt.show(block=False)
    plt.pause(1./30)


def main(population, bio_density):

    def generate_food(board, size: int) -> object:
        # Funkcja generująca jedzenie
        x = randrange(menu_width + size, screen_width - size, size)
        y = randrange(1 + size, screen_height - size, size)
        board[y//15][(x - menu_width)//15] = -1
        return Food(x, y)

    def new_food(board, food_frequency: float) -> None:
        '''
        Funkcja dodaje jedzenie na planszę.
        Im większe frequency tym mniej jedzenia się pojawi.
        '''
        food_width = int(5) # dla jedzenia o szerokości 5
        for i in range(int(bio_density * screen_height ** 2 // (food_frequency ** 2))):
            new_food = generate_food(board, food_width)
            while new_food in bugs:
                new_food = generate_food(board, food_width)
            bugs.add(new_food)
        # Szerokość jedzenia to 5, dlatego +/- 5, dzięki temu jedzenie na siebie nie na chodzi

    def new_ducks(number: int, width: int, height: int) -> None:
        '''
        Funkcja dodaje number kaczek do symulacji 
        W tym przypadku kaczki nachodzące na siebie nas nie dotyczy, bo ruch i tak
        tego nie uwzględnia.
        '''
        for i in range(number):
            ducks.add(
                Duck(
                    name = f"Kaczucha no {i}",
                    speed = randint(6, 10),
                    sense = 100,
                    energy = 3000,
                    x = randint(width, width + height),
                    y = randint(1, height),
                    group = ducks
                )
            )

    # inicjacja środowiska pygame owego
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Natural selection')
    clock = pygame.time.Clock()
    font = pygame.font.Font('font/Pixeltype.ttf', 50)

    # SEKCJE OKNA

    # intro screen

    duck_logo = pygame.image.load('graphics/duckies/front.png').convert_alpha()
    duck_logo = pygame.transform.rotozoom(duck_logo, 0, 4)
    duck_logo_rect = duck_logo.get_rect(center=(screen_width // 2, screen_height // 2))

    game_name = font.render('Ruber duck natural selection simulation', False, (0, 0, 0))
    game_name_rect = game_name.get_rect(center=(screen_width // 2, 300))

    game_message = font.render('Press space to run', False, (0, 0, 0))
    game_message_rect = game_message.get_rect(center=(screen_width // 2, 700))

    # tło do symulacji
    background_surf = pygame.image.load('graphics/bg2.jpg').convert()

    # obszar menu bocznego
    menu_surf = pygame.Surface((menu_width, screen_height))
    menu_surf.fill((255, 255, 255))

    pause_img = pygame.image.load('graphics/pause.png').convert_alpha()
    play_img = pygame.image.load('graphics/play.png').convert_alpha()
    pause_button = Button(menu_width // 2, 350, play_img)

    restart_button = Button(menu_width // 2, 450, pygame.image.load('graphics/restart.png').convert_alpha())

    # GENERACJA OBIEKTÓW

    # generowanie losowe kaczek
    ducks = pygame.sprite.Group()

    # generowanie losowe jedzenia
    bugs = pygame.sprite.Group()

    running = False
    intro = True

    # Timer
    food_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(food_timer, 4000)

    while True:

        # sprawdzanie inputu od urzytkownika
        for event in pygame.event.get():
            # zamykanie okna
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # pauza
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if not intro:
                    pause_start = int(pygame.time.get_ticks() / 1000) - pause_gap - start_time
                    pause_button.action = not pause_button.action
                    pause_button.image = pause_img if pause_button.action else play_img
                else:
                    intro = False
                    board = np.zeros((screen_height//15, screen_height//15), dtype=np.int32)

                    new_ducks(population, menu_width, screen_height)
                    new_food(board, 40)  # Początkowe jedzenie const = 20

                    # deklaracja wykresu
                    fig, ax = plt.subplots()

                    start_time = int(pygame.time.get_ticks() / 1000)
                    pause_button.action = False
                    pause_start = 0
                    pause_gap = 0

                running = not running


            if running:
                if event.type == food_timer:
                    new_food(board, 60)


        if running:
            # Wyświetlanie elementów symulacji

            # tło symulacji
            screen.blit(background_surf, (menu_width, 0))

            # menu
            screen.blit(menu_surf, (0, 0))
            display_score(screen, font, start_time, pause_gap)
            display_bio_density(screen, font, bio_density)
            display_population(screen, font, ducks)

            if pause_button.draw(screen):
                pause_start = int(pygame.time.get_ticks() / 1000) - pause_gap -start_time
                pause_button.image = pause_img
                running = not running

            if restart_button.draw(screen):
                restart_button.action = False
                ducks.empty()
                bugs.empty()
                intro = True
                running = False
                plt.close()

            # wykres
            draw_population_graph(ax, ducks)

            # bugs

            bugs.draw(screen)

            # ducks
            ducks.draw(screen)
            ducks.update(menu_width, (screen_width, screen_height), bugs)

            # sprawdzanie kolizji
            collision_sprite(ducks, bugs, board.shape[0], board.shape[1])

        elif intro:
            screen.fill((255, 255, 255))
            screen.blit(game_name, game_name_rect)
            screen.blit(duck_logo, duck_logo_rect)
            screen.blit(game_message, game_message_rect)

        else:
            screen.blit(menu_surf, (0, 0))
            frozen_time(screen, font, pause_start)
            display_bio_density(screen, font, bio_density)
            display_population(screen, font, ducks)

            if not pause_button.draw(screen):
                running = not running
                pause_button.image = play_img

            if restart_button.draw(screen):
                restart_button.action = False
                ducks.empty()
                bugs.empty()
                intro = True
                running = False
                plt.close()

            pause_gap = calculate_pause(pause_start + start_time)

        if len(ducks.sprites()) == 0 and not intro:
            running = False
            pause_start = int(pygame.time.get_ticks() / 1000) - pause_gap - start_time

        pygame.display.update()
        
        # ustawienie klatek na sekunde -> 30fps
        clock.tick(30)

    
if __name__ == '__main__':
    menu_width = 300

    screen_height = 1050
    screen_width = menu_width + screen_height
    
    main(population=20, bio_density=0.15)
