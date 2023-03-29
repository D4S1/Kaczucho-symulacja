import pygame
import math
from random import randint, choice, random


class Duck(pygame.sprite.Sprite):

    def __init__(self, name, speed, sense, energy, x, y, group):
        super().__init__()

        # PARAMETRY ORGANIZMU
        self.name = name

        self.speed = speed
        self.sense = sense
        self.energy = energy
        self.group = group

        # Koszt energii na 1 krok
        self.step_energy_cost = self.speed**2 + (self.sense / 0.5)

        # Koszt energii na rozmnażanie
        self.reproduction_energy_cost = 40 * self.step_energy_cost

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
        self.directions = {'down': (0, 1), 'up': (0, -1), 'right': (1, 0), 'left': (-1, 0), 'front': (0, 0)}
        self.duck_direction = 'front'
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

    def move(self, menu_width, screen_size):
        """
        funkcja modyfikująca współrzędne obiektu
        """

        # ustawienie nowego kierunku
        next_dir = self.duck_direction
        if random() < self.change_dir_probability:
            next_dir = choice(list(self.directions.keys()))
        self.animation_state(next_dir)

        # poruszamy się o self.speed pixli w danym kierunku
        # nowa pozycja x-owa += kierunke[0] * speed
        # możliwe kierunki -> (-1, 0), (0, -1), (1, 0), (0, 1), (0, 0)
        self.rect.x += self.directions[next_dir][0] * self.speed
        if self.rect.left < menu_width: self.rect.right = screen_size[0]
        if self.rect.right > screen_size[0]: self.rect.left = menu_width

        # tak samo ja wyżej tylko, że dla y
        self.rect.y += self.directions[next_dir][1] * self.speed
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
        speed = self.speed
        sense = self.sense

        if random() < self.mutation_probability:
            if speed <= 1 or random() >= 0.5:
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
                    energy=4 * self.reproduction_energy_cost,
                    x=self.rect.x,
                    y=self.rect.y,
                    group=self.group
                )
            )

    def eat(self):
        self.energy += 100

    def alive(self):
        if self.energy <= 0:
            self.kill()

    def update(self, menu_width, screen_size):
        self.move(menu_width, screen_size)
        self.energy_lost()
        self.reproduce()
        self.alive()
