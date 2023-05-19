import pygame
import math
from random import randint, choice, random


class Duck(pygame.sprite.Sprite):

    def __init__(self, name, speed, sense, energy, x, y, group):
        super().__init__()

        # PARAMETRY ORGANIZMU
        self.name = name

        # target
        self.target = None
        self.dx = 0
        self.dy = 0

        self.speed = speed
        self.sense = sense

        self.energy = energy
        self.group = group

        # Koszt energii na 1 krok
        self.step_energy_cost = self.speed**2 / 1.5

        # Koszt energii na rozmnażanie
        self.reproduction_energy_cost = 20 * self.step_energy_cost

        # Prawdopodobieństwo, że zajdzie mutacja przy rozmnażaniu
        self.mutation_probability = 0.5

        # Prawdopodobieńśtwo, że kaczucha zmieni kierunek
        self.change_dir_probability = 0.3

        # GRAFIKI DO ANIMACJI
        self.frames = {
        'front': [pygame.image.load('graphics/duckies/front.png').convert_alpha()],
        'back': [pygame.image.load('graphics/duckies/back.png').convert_alpha()],
        'down': [
            pygame.image.load('graphics/duckies/front-walk-1.png').convert_alpha(),
            pygame.image.load('graphics/duckies/front-walk-2.png').convert_alpha(),
            pygame.image.load('graphics/duckies/front-walk-3.png').convert_alpha(),
            pygame.image.load('graphics/duckies/front-walk-4.png').convert_alpha(),
        ],
        'up': [
            pygame.image.load('graphics/duckies/back-walk-1.png').convert_alpha(),
            pygame.image.load('graphics/duckies/back-walk-2.png').convert_alpha(),
            pygame.image.load('graphics/duckies/back-walk-3.png').convert_alpha(),
            pygame.image.load('graphics/duckies/back-walk-4.png').convert_alpha(),
        ],
        'right': [
            pygame.image.load('graphics/duckies/side-walk-1.png').convert_alpha(),
            pygame.image.load('graphics/duckies/side-walk-2.png').convert_alpha(),
            pygame.image.load('graphics/duckies/side-walk-3.png').convert_alpha(),
            pygame.image.load('graphics/duckies/side-walk-4.png').convert_alpha(),
        ],
        }
        self.frames['left'] = [pygame.transform.flip(img, True, False) for img in self.frames['right']]

        # ustawienie stanu animacji
        self.directions = {'down': (0, 1), 'up': (0, -1), 'right': (1, 0), 'left': (-1, 0)}
        self.duck_direction = choice(list(self.directions.keys()))
        self.duck_frame_idx = 0

        # Pygame owe rzeczy
        self.image = self.frames['front'][0]
        self.rect = self.image.get_rect(midbottom=(x, y))

    def animation_state(self, next_dir):
        """
        funkcja ustawia, która z grafik animacji powinna zostać w danej klatce wyświetlona
        """
        if next_dir != self.duck_direction: 
            self.duck_frame_idx = 0
            self.duck_direction = next_dir

        # chcemu żeby nowa grafika się pojawiała co kilka klatek
        self.duck_frame_idx += 0.2
        if self.duck_frame_idx >= len(self.frames[self.duck_direction]): self.duck_frame_idx = 0

        self.image = self.frames[self.duck_direction][int(self.duck_frame_idx)]

    def check_food(self, board, lista: list) -> tuple:
        rows, columns = board.shape[0], board.shape[1]
        for y, x in lista:
            if board[y % rows][x % columns] == -1:
                return y % rows, x % columns

    def closest_food(self, board, menu_width):
        """
        NIEAKTUALNY OPIS
        Funkcja przyjmuje współrzędne kaczki oraz jej sense
        Zwraca krotkę, gdzie są współrzędne najbliższego jedzenia,
        ewentualnie None, jeśli jedzenia nie znalazł
        oraz int czyli liczbe ruchów potrzebnej kaczce do tego ruchu...
        Program działa dla kaczki zwróconej na wprost (w góre), jeśli kaczka
        jest zwrócona na dół to trzeba y + 1, a jak w prawo i w lewo to analogicznie
        tylko swap x oraz y
        """
        dir = self.directions[self.duck_direction]
        rows, columns = board.shape[0], board.shape[1]
        coordinates = [[self.rect.y//15, (self.rect.x - menu_width)//15]]

        for i in range(1, self.sense + 1):

            for j in range(0, len(coordinates)):
                coordinates[j][0], coordinates[j][1] = (coordinates[j][0] + dir[1]) % rows, (coordinates[j][1] + dir[0]) % columns

            coordinates.append([coordinates[0][0] + dir[0] * i, (coordinates[0][1] + dir[1] * i) % columns])
            coordinates.append([coordinates[0][0] - dir[0] * i, (coordinates[0][1] - dir[1] * i) % columns])
            check = self.check_food(board, coordinates)

            if check:
                print(f"{self.name}\t{check=}")
                return check

    def move_to_target(self, menu_width):
        next_dir = self.duck_direction
        # print(f"=====================\n BEFORE {self.duck_direction=}")
        # print(f"{self.name=}    {self.sense=}    {self.target=} {(self.rect.x - menu_width)//15=} {self.rect.y//15=}")
        if next_dir in ['up', 'down']:
            if next_dir == 'up' and self.rect.y//15 < self.target[0] or next_dir == 'down' and self.rect.y//15 > self.target[0]:
                self.rect.y = self.target[0] * 15
            if self.target[0] == self.rect.y//15:
                next_dir = 'left' if self.target[1] <= (self.rect.x - menu_width) else 'right'

        elif next_dir in ['left', 'right']:
            if next_dir == 'left' and self.rect.x//15 < self.target[1] or next_dir == 'right' and self.rect.x//15 > self.target[1]:
                self.rect.x = self.target[1] * 15 + menu_width

            if self.target[1] == (self.rect.x - menu_width)//15:
                next_dir = 'up' if self.target[0] <= self.rect.y else 'down'
        self.animation_state(next_dir)
        # print(f"AFTER {self.duck_direction=}\n =============================")

    def random_dir(self):
        # ustawienie nowego kierunku
        next_dir = self.duck_direction
        if random() < self.change_dir_probability:
            next_dir = choice(list(self.directions.keys()))
        self.animation_state(next_dir)

    def move(self, menu_width, screen_size):
        """
        funkcja modyfikująca współrzędne obiektu
        """
        # poruszamy się o self.speed pixli w danym kierunku
        # nowa pozycja x-owa += kierunke[0] * speed
        # możliwe kierunki -> (-1, 0), (0, -1), (1, 0), (0, 1), (0, 0)
        self.rect.x += self.directions[self.duck_direction][0] * self.speed
        if self.rect.left < menu_width: self.rect.right = screen_size[0]
        if self.rect.right > screen_size[0]: self.rect.left = menu_width

        # tak samo ja wyżej tylko, że dla y
        self.rect.y += self.directions[self.duck_direction][1] * self.speed
        if self.rect.top < 0: self.rect.bottom = screen_size[1]
        if self.rect.bottom > screen_size[1]: self.rect.top = 0

    def energy_lost(self):
        '''
        Koszt energii w jednej jednostce czasu, jaki ponosi
        organizm. W przypadku jeśli spadnie to zera to
        kaczucha umiera.
        energy = enrgy - (speed^2 * sense)
        '''
        self.energy -= self.step_energy_cost

    def mutate(self):
        """
        Funkcja generuje zmutowane (lub nie) parametry dla potomstwa
        """
        speed = self.speed
        sense = self.sense

        if random() < self.mutation_probability:
            if speed <= 3 or random() >= 0.5:
                speed += math.ceil(0.1 * speed)
            else:
                speed -= math.ceil(0.1 * speed)

            if sense <= 1 or random() >= 0.5:
                sense += 1
            else:
                sense -= 1

        return speed, sense

    def reproduce(self):
        """
        funkcja rozmnażająca kaczki
        warto się zastanowić nad energią graniczną wymaganą do rozmnażania,
        energią zużywaną na rozmnażanie i energią nadawaną dzieciom
        """
        if self.energy >= 5 * self.reproduction_energy_cost:
            self.energy -= self.reproduction_energy_cost
            speed, sense = self.mutate()
            self.group.add(
                Duck(
                    name=f"Kaczucha",
                    speed=speed,
                    sense=sense,
                    energy=2 * self.reproduction_energy_cost,
                    x=self.rect.x,
                    y=self.rect.y,
                    group=self.group
                )
            )

    def eat(self):
        self.energy += 500

    def alive(self):
        if self.energy <= 0:
            self.kill()

    def update(self, menu_width, screen_size, board):
        next_target = self.closest_food(board, menu_width)

        if self.target is None or next_target is not None and (next_target[0]**2 + next_target[1]**2)**1/2 < (self.target[0]**2 + self.target[1]**2)**1/2:
            self.target = next_target

        if self.target is not None:
            # print(f"Jestem na tropie")
            self.move_to_target(menu_width)
        else:
            # print(f"chodze randomowo-> essa")
            self.random_dir()

        self.move(menu_width, screen_size)
        self.energy_lost()
        self.reproduce()
        self.alive()
