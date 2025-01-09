import random
import numpy as np
from Selection import Selection
from Crossover import Crossover  # Importăm clasa Crossover
from TSP_Data import TSPData

class Main:
    def __init__(self, tsp_data_file):
        """
        Inițializează clasa principală pentru TSP, încărcând datele și configurând algoritmul evoluționar.

        :param tsp_data_file: Calea către fișierul care conține datele TSP
        """
        # Încărcăm datele din fișier folosind clasa TSPData
        self.tsp_data = TSPData(tsp_data_file)

        # Inițializăm populația
        self.population_size = 100  # Mărimea populației
        self.population = self.initialize_population()

        # Creăm instanța de selecție
        self.selection = Selection(self.population, self.fitness_function, tournament_size=5)

        # Creăm instanța de crossover
        self.crossover = Crossover()

    def initialize_population(self):
        """
        Inițializează populația aleatorie de soluții (ordinea orașelor).

        :return: O listă de soluții (populația)
        """
        population = []
        for _ in range(self.population_size):
            # Creăm o soluție randomizată: o permutare aleatorie a orașelor
            solution = list(
                range(len(self.tsp_data.get_coordinates())))  # Orașele sunt indexate de la 0 la numărul de orașe - 1
            random.shuffle(solution)  # Permutăm orașele aleatoriu
            population.append(solution)
        return population

    def fitness_function(self, solution):
        """
        Calculează fitness-ul unei soluții (distanta totală în problema TSP).

        :param solution: Soluția curentă (o permutare a orașelor)
        :return: Distanta totală (fitness-ul soluției)
        """
        return self.calculate_total_distance(solution)

    def calculate_total_distance(self, solution):
        """
        Calculează distanța totală pentru o soluție dată (un traseu de orașe).

        :param solution: O soluție - o listă de indici ai orașelor
        :return: Distanța totală
        """
        total_distance = 0
        for i in range(len(solution) - 1):
            total_distance += self.tsp_data.get_distance(solution[i], solution[i + 1])
        total_distance += self.tsp_data.get_distance(solution[-1], solution[0])  # Întoarcerea la început
        return total_distance

    def evolve(self, generations=100):
        """
        Execută algoritmul evoluționar pentru un anumit număr de generații.

        :param generations: Numărul de generații pentru evoluție
        """
        for generation in range(generations):
            print(f"\nGenerația {generation + 1} - Selecție părinți:")

            # Selectăm părinții pentru a forma noi soluții
            parents = self.selection.select_population(2)

            # Afișăm părinții selectați pentru această generație
            print("Părinții selectați: ")
            for parent in parents:
                print(f"Individ: {parent} - Distanță: {self.fitness_function(parent)}")

            # Aplicați operatorul de crossover pentru a crea copii din părinți
            children = self.crossover.crossover_population(parents)

            # Afișăm copiii creați
            print("Copii creați prin crossover: ")
            for child in children:
                print(f"Individ: {child} - Distanță: {self.fitness_function(child)}")

            # Înlocuirea populației cu noii copii
            self.population = children

            # Afișăm fitness-ul pentru fiecare generație (pentru a urmări progresul)
            best_solution = min(self.population, key=self.fitness_function)
            best_fitness = self.fitness_function(best_solution)
            print(f"Generația {generation + 1} - Best fitness: {best_fitness}")

    def run(self, generations=100):
        """
        Rulează algoritmul evoluționar.

        :param generations: Numărul de generații pentru evoluție
        """
        print("Începerea evoluției TSP...")
        self.evolve(generations)
        print("Evoluția s-a încheiat.")


# Exemplu de utilizare
if __name__ == "__main__":
    # Calea către fișierul TSP
    tsp_data_file = "ch130.tsp"  # Înlocuiește cu calea fișierului TSP

    # Inițializăm și rulăm algoritmul
    main_algorithm = Main(tsp_data_file)
    main_algorithm.run(generations=100)
