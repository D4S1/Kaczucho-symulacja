import pygame
from sys import exit
from random import randint

from duck import Duck
from food import Food


# === MENU ===
def display_score(screen, font, start_time):
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = font.render(f'Time: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(menu_width//2, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def display_bio_density(screen, font, bio_density):
    score_surf = font.render(f'Bio_density: {bio_density}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(menu_width//2, 150))
    screen.blit(score_surf, score_rect)


def display_population(screen, font, ducks):
    score_surf = font.render(f'Populacja: {len(ducks.sprites())}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(menu_width//2, 250))
    screen.blit(score_surf, score_rect)


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


def main(population, bio_density):

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

    pause_surf = pygame.image.load('graphics/pause.png').convert_alpha()
    pause_rect = pause_surf.get_rect(center=(menu_width // 2, 350))

    play_surf = pygame.image.load('graphics/play.png').convert_alpha()
    play_rect = play_surf.get_rect(center=(menu_width // 2, 350))

    restart_surf = pygame.image.load('graphics/restart.png').convert_alpha()
    restart_rect = restart_surf.get_rect(center=(menu_width // 2, 450))

    # GENERACJA OBIEKTÓW

    # generowanie losowe kaczek
    ducks = pygame.sprite.Group()
    for i in range(population):
        ducks.add(
            Duck(
                name=f"Kaczucha no {i}",
                speed=randint(4, 8),
                energy=15000,
                x=randint(menu_width, screen_width),
                y=randint(1, screen_height)
            )
        )

    # generowanie losowe jedzenia
    bugs = pygame.sprite.Group()
    for i in range(int(bio_density * (screen_height ** 2) // (20 * 20))):
        bugs.add(Food(x=randint(menu_width, screen_width), y=randint(1, screen_height)))

    running = False
    intro = True

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
                running = not running
                intro = False

        if running:
            # Wyświetlanie elementów symulacji

            # tło symulacji
            screen.blit(background_surf, (menu_width, 0))

            # menu
            screen.blit(menu_surf, (0, 0))
            score = display_score(screen, font, start_time)
            display_bio_density(screen, font, bio_density)
            display_population(screen, font, ducks)
            screen.blit(play_surf, play_rect)
            screen.blit(restart_surf, restart_rect)

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

        pygame.display.update()
        
        # ustawienie klatek na sekunde -> 30fps
        clock.tick(30)

    
if __name__ == '__main__':
    menu_width = 300

    screen_height = 800
    screen_width = menu_width + screen_height

    main(40, 0.2)
