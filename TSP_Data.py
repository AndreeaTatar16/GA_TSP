import numpy as np
import math

class TSPData:
    def __init__(self, filename):
        self.filename = filename
        self.coordinates, self.distances = self.read_file()

    def read_file(self):
        coordinates = []
        with open(self.filename, 'r') as file:
            lines = file.readlines()
            # Căutăm secțiunea NODE_COORD_SECTION
            start_reading = False
            for line in lines:
                line = line.strip()
                if line == "NODE_COORD_SECTION":
                    start_reading = True
                    continue
                if line == "EOF":
                    break
                if start_reading:
                    # Citim coordonatele x, y pentru fiecare oraș
                    parts = line.split()
                    city_id = int(parts[0])
                    x = float(parts[1])
                    y = float(parts[2])
                    coordinates.append((x, y))

        # Creăm matricea de distanțe
        n = len(coordinates)
        distances = np.zeros((n, n))  # inițializăm matricea cu 0

        # Calculăm distanțele pentru fiecare pereche de orașe
        for i in range(n):
            for j in range(i + 1, n):  # doar pentru j > i, pentru a evita calculul redundant
                dist = self.euclidean_distance(coordinates[i], coordinates[j])
                distances[i][j] = dist
                distances[j][i] = dist  # distanța între i și j este aceeași ca între j și i

        # # Afișăm matricea de distanțe
        # print("Matricea de distanțe (distantele dintre orașe):")
        # print(distances)

        return coordinates, distances

    def euclidean_distance(self, city1, city2):
        x1, y1 = city1
        x2, y2 = city2

        return math.sqrt(((x1 - x2)*(x1 - x2)) + ((y1 - y2)*(y1 - y2)))

    def get_distance(self, city1, city2):
        #print(f"city1: {city1}, city2: {city2}")
        #print(self.distances[city1][city2])
        return self.distances[city1][city2]

    def get_coordinates(self):
        return self.coordinates
