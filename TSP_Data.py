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
        distances = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                if i != j:
                    distances[i][j] = self.euclidean_distance(coordinates[i], coordinates[j])

        return coordinates, distances

    def euclidean_distance(self, city1, city2):
        x1, y1 = city1
        x2, y2 = city2
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    def get_distance(self, city1, city2):
        return self.distances[city1][city2]

    def get_coordinates(self):
        return self.coordinates
