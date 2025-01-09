import math
import random

class Selection:
    def __init__(self, population, fitness_function, tournament_size, coordinates):
        """
        Inițializează clasa de selecție.

        :param population: Lista de soluții (indivizi) din populație
        :param fitness_function: Funcția de fitness care calculează valoarea fitness-ului pentru o soluție
        :param tournament_size: Dimensiunea turneului (câte soluții vor participa la selecție)
        :param coordinates: Coordonatele orașelor (lista de perechi x, y)
        """
        self.population = population
        self.fitness_function = fitness_function
        self.tournament_size = tournament_size
        self.coordinates = coordinates  # Lista de coordonate pentru orașe

    def select_parents(self):
        """
        Selectează doi părinți folosind selecția prin turneu.

        :return: 2 părinți selectați din populație
        """
        # Selectăm un turneu de soluții aleatorii
        tournament = random.sample(self.population, self.tournament_size)

        # Sortăm turneul după fitness (mai bine este mai mică distanța pentru TSP)
        tournament_sorted = sorted(tournament, key=self.fitness_function, reverse=False)

        # Returnăm primii doi părinți din turneu
        parent1 = tournament_sorted[0]
        parent2 = tournament_sorted[1]

        return parent1, parent2

    def select_population(self, num_parents):
        """
        Selectează o populație de părinți pentru încrucișare (poate fi folosită pentru întreaga generație).

        :param num_parents: Numărul de părinți necesari
        :return: O listă de părinți selectați
        """
        parents = []
        for _ in range(num_parents // 2):  # Selectăm 2 părinți la fiecare iterație
            parent1, parent2 = self.select_parents()

            # Aplică 2-opt pe părinți pentru a-i îmbunătăți
            parent1 = self.two_opt(parent1)
            parent2 = self.two_opt(parent2)

            parents.append(parent1)
            parents.append(parent2)

        return parents

    def two_opt(self, route):
        """
        Aplica operatorul 2-opt pe traseul dat pentru a îmbunătăți distanța.

        :param route: Traseul curent (lista de orașe)
        :return: Traseul îmbunătățit
        """
        best_route = route
        best_distance = self.calculate_total_distance(route)

        # Explorează toate perechile de muchii și înlocuiește-le
        for i in range(1, len(route) - 1):
            for j in range(i + 1, len(route)):
                new_route = route[:i] + route[i:j + 1][::-1] + route[j + 1:]
                new_distance = self.calculate_total_distance(new_route)

                if new_distance < best_distance:
                    best_route = new_route
                    best_distance = new_distance

        return best_route

    def calculate_total_distance(self, route):
        """
        Calculează distanța totală a unui traseu, având în vedere distanța între fiecare pereche de orașe.

        :param route: Traseul (lista de orașe)
        :return: Distanța totală
        """
        distance = 0
        for i in range(len(route) - 1):
            # Calculează distanța între două orașe consecutive
            distance += self.get_distance(route[i], route[i + 1])
        # Adaugă distanța între ultimul oraș și primul (ciclul TSP)
        distance += self.get_distance(route[-1], route[0])
        return distance

    def get_distance(self, city1, city2):
        """
        Returnează distanța dintre două orașe utilizând coordonatele lor.

        :param city1: Indexul primului oraș
        :param city2: Indexul celui de-al doilea oraș
        :return: Distanța între cele două orașe
        """
        x1, y1 = self.coordinates[city1]
        x2, y2 = self.coordinates[city2]
        return math.sqrt(((x1 - x2)*(x1 - x2)) + ((y1 - y2)*(y1 - y2)))
