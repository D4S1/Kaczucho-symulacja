import numpy as np
from random import randint


def test_sense(rows: int, columns: int):
    board = np.zeros((rows, columns), dtype=np.int32)

    def generating_food(number: int) -> None:
        # -1 na macierzy to jedzenie
        for i in range(number):
            x = randint(0, columns - 1)
            y = randint(0, rows - 1)
            while board[y][x] != 0:
                x = randint(0, columns - 1)
                y = randint(0, rows - 1)
            board[y][x] = -1

    def generation_duck(number: int) -> tuple:
    	# 1 na macierzy to kaczka
        for i in range(number):
            x = randint(0, columns - 1)
            y = randint(0, rows - 1)
            while board[y][x] != 0:
                x = randint(0, columns - 1)
                y = randint(0, rows - 1)
            board[y][x] = 1
            return (y, x)

    generating_food(4)
    duck_y, duck_x = generation_duck(2)
    print(board)
    print('Współrzędne kaczki: ', duck_y, duck_x)
    
    def check_food(lista: list) -> tuple:
        for el in lista:
            if board[el[0] % rows][el[1] % columns] == -1:
                return (el[0] % rows, el[1] % columns)
        return None

    def closest_food(y: int, x: int, sense: int) -> (tuple, int):
        '''
        Funkcja przyjmuje współrzędne kaczki oraz jej sense
        Zwraca krotkę, gdzie są współrzędne najbliższego jedzenia, 
        ewentualnie None, jeśli jedzenia nie znalazł
        oraz int czyli liczbe ruchów potrzebnej kaczce do tego ruchu...
        Program działa dla kaczki zwróconej na wprost (w góre), jeśli kaczka
        jest zwrócona na dół to trzeba y + 1, a jak w prawo i w lewo to analogicznie
        tylko swap x oraz y
        '''
        coordinates = [[(y - 1) % rows, x % columns]]
        check = check_food(coordinates)
        for i in range(1, sense):
            if check:
                #print(i, coordinates)
                return check, i
            if i % 2 == 0:
                coordinates.pop(-1)
                coordinates.pop(-1)
            for j in range(1, len(coordinates)):
                if j % 2 == 1:
                    coordinates[j][1] = (coordinates[j][1] + 1) % columns
                else:
                    coordinates[j][1] = (coordinates[j][1] - 1) % columns

            coordinates.insert(1, [coordinates[0][0], (coordinates[0][1] - 1) % columns])
            coordinates.insert(1, [coordinates[0][0], (coordinates[0][1] + 1) % columns])
            coordinates[0] = [(coordinates[0][0] - 1), coordinates[0][1]]
            check = check_food(coordinates)
            #print('Pętla: ', coordinates)
        return None
    
    return(closest_food(duck_y, duck_x, 8))

# krotka to współrzędne punktu, najlbiższego jedzenia, jak None to znaczy, że nie ma jedzenia w zasięgu
# druga wartość zwraca liczbę ruchów
print(test_sense(10, 10))
