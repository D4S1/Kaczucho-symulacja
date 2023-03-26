import pygame
from sys import exit
from random import randint

from duck import Duck
from food import Food


# ============== MENU ==============
def display_score(screen, font, start_time):
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = font.render(f'Time: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(100, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def display_bio_density(screen, font, bio_density):
    score_surf = font.render(f'Bio_density: {bio_density}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(100, 150))
    screen.blit(score_surf, score_rect)


def display_population(screen, font, ducks):
    score_surf = font.render(f'Populacja: {len(ducks.sprites())}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(100, 250))
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
    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption('Natural selection')
    clock = pygame.time.Clock()
    font = pygame.font.Font('font/Pixeltype.ttf', 50)

    # SEKCJE OKNA

    # tło do symulacji
    background_surf = pygame.image.load('graphics/bg1.png').convert()

    # obszar menu bocznego
    menu_surf = pygame.Surface((200, 800))
    menu_surf.fill((255, 255, 255))

    # GENERACJA OBIEKTÓW

    # generowanie losowe kaczek
    ducks = pygame.sprite.Group()
    for i in range(population):
        ducks.add(Duck(name=f"Kaczucha no {i}", speed=randint(4, 8), energy=15000, x=randint(200, 1000), y=randint(1, 800)))

    # generowanie losowe jedzenia
    bugs = pygame.sprite.Group()
    for i in range(int(bio_density * (800 * 800) // (20 * 20))):
        bugs.add(Food(x=randint(200, 1000), y=randint(1, 800)))

    running = True
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

        if running:
            # Wyświetlanie elementów symulacji

            # tło symulacji
            screen.blit(background_surf, (200, 0))

            # menu
            screen.blit(menu_surf, (0, 0))
            score = display_score(screen, font, start_time)
            display_bio_density(screen, font, bio_density)
            display_population(screen, font, ducks)

            # bugs
            bugs.draw(screen)

            # ducks
            ducks.draw(screen)
            ducks.update()

            # sprawdzanie kolizji
            collision_sprite(ducks, bugs)

        pygame.display.update()
        
        # ustawienie klatek na sekunde -> 30fps
        clock.tick(30)

    
if __name__ == '__main__':
    main(40, 0.2)
