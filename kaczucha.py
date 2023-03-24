import random # do losowania wartości

class Kaczucha:

    def __init__(self, speed: int, sense: float, energy: float):

        self.speed = speed # liczba wektorów losowanych w jednej jednostce czasu
        self.sense = sense 
        self.energy = energy
        self.position = (0, 0)

    def update_speed(self: object, percent: float, update_value: float) -> float:
        '''

        Liczba pól pokonywanych w jednej jednostce czasu,
        zakładam, że ruch nie jest diagonalny.
        '''
        if random.random() <= percent:
            if random.randint(0, 1):
                self.speed += 1 # Wzrasta liczba wektorów
            else:
                self.speed -= 1 # Maleje liczba wektorów

    def update_sense(self: object, percent: float) -> float:
        '''
        możliwość wykrywania jedzenia, plansza to macierz
        zatem należy ustalić sense wertykalnie oraz diagonalnie
        Np. sense = 2 oznacza, że kaczucha wyczuwa jedzenie w zesięgu
        2 we wszystkich 8 kierunkach, a jak sense = 2.5 to dodatkowo wertykalnie
        na odległość 3
        Alternatywnie rozpatrzyć ściśle 8 kierunków...
        '''
        if random.random() <= percent:
            if random.randint(0, 1):
                self.sense += 0.5
            else:
                self.sense -= 0.5

    def update_energy(self: object, energy: float) -> float:
        '''
        Koszt energii w jednej jednostce czasu, jaki ponosi
        organizm. W przypadku jeśli spadnie to zera to
        kaczucha umiera.
        energy = enrgy - (speed^2 * sense)
        '''
        self.energy -= self.speed**2 * (self.sense / 0.5)

    def move(self: object):
        '''
        W jednej jednostce czasu losujemy [speed] wektorów
        o długości jeden, a następnie przemieszczamy kaczuchę.
        Ogólnie zakładamy inteligencje gatunkową, jesli chodzi
        o powrót...
        
        1) Losujemy z czterech wektorów: (1, 0); (0, 1); (-1, 0); (0, -1)
           oczywiście, tak, aby ruch kaczuchy miał sens (pierwszy ruch jest
           wymuszony, ponieważ musi się umieścić na planszy)
        2) Następnie losujemy kolejny wektor, ale zabroniony jest ruch przeciwny
        3) Jeśli kaczucha ma jedno jedzenie to szuka drugiego, pod warunkiem, że może
           tzn. (inteligencja kaczuchy) wraca do najbliższej krawędzi
        4) Jeśli nie ma jedzenia to szuka dalej...
        '''
        pass
