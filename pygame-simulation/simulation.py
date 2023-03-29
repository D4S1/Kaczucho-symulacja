import pygame
from sys import exit
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
    return len(ducks.sprites())


# === HELPER FUNCTIONS ===

def collision_sprite(ducks, bugs):
    """
    Funkcja sprawdza kolizje pomiędzy obiektami (czyt. czy kaczka weszła na bug'a)
    Jeżeli tak, to zwiększy energie kaczki i usunie obiekt bug'a
    :param ducks:
    :param bugs:
    :return: None
    """
    for duck in ducks.sprites():
        if pygame.sprite.spritecollide(duck, bugs, True):
            duck.eat()


# === GRAPH ===

def draw_population_graph(ax, group):
    """
    Funkcja rysuje wykres.
    Promień koła odpowiada liczbie kaczek o danych atryburach.
    :param ax:
    :param group:
    :return:
    """
    x = [duck.speed for duck in group]
    y = [duck.sense for duck in group]
    count = Counter(zip(x, y))
    size = [50 * count[(x1, y1)] for x1, y1 in zip(x, y)]
    ax.clear()
    ax.set(xlim=(0, 15), ylim=(0, 10), xlabel="speed", ylabel="sense", title="Populacja kaczek")
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 10)
    ax.scatter(x, y, s=size)
    plt.show(block=False)
    plt.pause(1./30)


def main(population, bio_density):

    def generate_food(size: int) -> object:
        # Funkcja generująca jedzenie
        return Food(x = randrange(menu_width + size, screen_width - size, size),
                    y = randrange(1 + size, screen_height - size, size))

    def new_food(food_frequency: float) -> None:
        '''
        Funkcja dodaje jedzenie na planszę.
        Im większe frequency tym mniej jedzenia się pojawi.
        '''
        food_width = int(5) # dla jedzenia o szerokości 5
        for i in range(int(bio_density * screen_height ** 2 // (food_frequency ** 2))):
            new_food = generate_food(food_width)
            while new_food in bugs:
                new_food = generate_food(food_width)
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
                    name=f"Kaczucha no {i}",
                    speed=randint(7, 12),
                    sense=randint(1, 5),
                    energy=15000,
                    x=randint(width, width + height),
                    y=randint(1, height),
                    group=ducks
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
    game_name_rect = game_name.get_rect(center=(screen_width // 2, 200))

    game_message = font.render('Press space to run', False, (0, 0, 0))
    game_message_rect = game_message.get_rect(center=(screen_width // 2, 600))

    # tło do symulacji
    background_surf = pygame.image.load('graphics/bg1.png').convert()

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
    new_ducks(population, menu_width, screen_height)

    # generowanie losowe jedzenia
    bugs = pygame.sprite.Group()
    new_food(20) # Początkowe jedzenie const = 20

    # deklaracja wykresu
    fig, ax = plt.subplots()

    running = False
    intro = True

    start_time = 0
    pause_start = 0
    pause_gap = 0

    # Timer
    food_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(food_timer, 4000)

    pause = False
    start_time = 0


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
                    pause_start = int(pygame.time.get_ticks() / 1000) - pause_start
                    pause_button.action = not pause_button.action
                    pause_button.image = pause_img if pause_button.action else play_img

                running = not running
                intro = False

            if running:
                if event.type == food_timer:
                    new_food(40)


        if running:
            # Wyświetlanie elementów symulacji

            # tło symulacji
            screen.blit(background_surf, (menu_width, 0))

            # menu
            screen.blit(menu_surf, (0, 0))
            display_score(screen, font, start_time, pause_gap)
            display_bio_density(screen, font, bio_density)
            population = display_population(screen, font, ducks)

            if pause_button.draw(screen):
                pause_start = int(pygame.time.get_ticks() / 1000) - pause_start
                pause_button.image = pause_img
                running = not running

            if restart_button.draw(screen):
                restart_button.action = False
                intro = True
                running = False
                start_time = int(pygame.time.get_ticks() / 1000)

            # wykres
            draw_population_graph(ax, ducks)

            # bugs

            bugs.draw(screen)

            # ducks
            ducks.draw(screen)
            ducks.update(menu_width, (screen_width, screen_height))

            # sprawdzanie kolizji
            collision_sprite(ducks, bugs)

        elif intro:
            screen.fill((255, 255, 255))
            screen.blit(game_name, game_name_rect)
            screen.blit(duck_logo, duck_logo_rect)
            screen.blit(game_message, game_message_rect)

        else:
            screen.blit(menu_surf, (0, 0))
            frozen_time(screen, font, pause_start)
            display_bio_density(screen, font, bio_density)
            population = display_population(screen, font, ducks)

            if not pause_button.draw(screen):
                running = not running
                pause_button.image = play_img

            restart_button.draw(screen)
            pause_gap = calculate_pause(pause_start)

        if population == 0:
            running = False
        pygame.display.update()
        
        # ustawienie klatek na sekunde -> 30fps
        clock.tick(30)


    
if __name__ == '__main__':
    menu_width = 300

    screen_height = 800
    screen_width = menu_width + screen_height
    
    main(40, 0.3)
