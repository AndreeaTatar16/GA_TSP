import random


class Selection:
    def __init__(self, population, fitness_function, tournament_size=5):
        """
        Inițializează clasa de selecție.

        :param population: Lista de soluții (indivizi) din populație
        :param fitness_function: Funcția de fitness care calculează valoarea fitness-ului pentru o soluție
        :param tournament_size: Dimensiunea turneului (câte soluții vor participa la selecție)
        """
        self.population = population
        self.fitness_function = fitness_function
        self.tournament_size = tournament_size

    def select_parents(self):
        """
        Selectează doi părinți folosind selecția prin turneu.

        :return: 2 părinți selectați din populație
        """
        # Selectăm un turneu de soluții aleatorii
        tournament = random.sample(self.population, self.tournament_size)

        # Sortăm turneul după fitness (mai bine este mai mică distanța pentru TSP)
        tournament_sorted = sorted(tournament, key=self.fitness_function, reverse=True)

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
            parents.append(parent1)
            parents.append(parent2)

        return parents
