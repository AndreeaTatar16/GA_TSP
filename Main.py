import concurrent

import matplotlib.pyplot as plt
import random
import numpy as np
from Mutation import Mutation
from Selection import Selection
from Crossover import Crossover
from TSP_Data import TSPData
from concurrent.futures import ThreadPoolExecutor

class Main:
    def __init__(self, tsp_data_file):
        """
        Inițializează clasa principală pentru TSP, încărcând datele și configurând algoritmul evoluționar.
        """
        # Încărcăm datele din fișier folosind clasa TSPData
        self.tsp_data = TSPData(tsp_data_file)

        # Creăm o matrice de distanțe între orașe pentru a evita calculul repetat
        self.distance_cache = {}
        self._generate_distance_cache()

        # Inițializăm populația
        self.population_size = 100  # Populația inițială
        self.max_population_size = 200  # Populația maximă
        self.population = self.initialize_population()

        # Creăm instanța de selecție
        self.selection = Selection(self.population, self.fitness_function, tournament_size=10,
                                   coordinates=self.tsp_data.get_coordinates())

        # Creăm instanța de crossover
        self.crossover = Crossover(self.tsp_data)

        # Listă pentru salvarea celor mai bune soluții, soluțiilor medii și celor mai slabe soluții
        self.best_solutions = []
        self.avg_solutions = []
        self.worst_solutions = []
        self.best_paths = []  # Listă pentru salvarea celor mai bune trasee
        self.worst_paths = []  # Listă pentru salvarea celor mai slabe trasee

        # Creăm instanța de mutație
        self.mutation = Mutation(mutation_rate=0.3)  # 50% șanse de mutație

    def _generate_distance_cache(self):
        """
        Generează un cache pentru distanțele între toate orașele.
        """
        num_cities = len(self.tsp_data.get_coordinates())
        for i in range(num_cities):
            for j in range(i + 1, num_cities):
                dist = self.tsp_data.get_distance(i, j)
                self.distance_cache[(i, j)] = dist
                self.distance_cache[(j, i)] = dist

    def calculate_total_distance(self, solution):
        """
        Calculează distanța totală pentru o soluție dată (un traseu de orașe) folosind cache-ul.
        """
        total_distance = 0
        for i in range(len(solution) - 1):
            total_distance += self.distance_cache[(solution[i], solution[i + 1])]
        total_distance += self.distance_cache[(solution[-1], solution[0])]  # Întoarcerea la început
        return total_distance

    def fitness_function(self, solution):
        """
        Calculează fitness-ul unei soluții (distanta totală în problema TSP).
        """
        return self.calculate_total_distance(solution)

    def initialize_population(self):
        """
        Inițializează populația aleatorie de soluții (ordinea orașelor).
        """
        population = []
        for _ in range(self.population_size):
            solution = list(range(len(self.tsp_data.get_coordinates())))
            random.shuffle(solution)
            population.append(solution)
        return population

    def evolve(self, generations=100):
        """
        Execută algoritmul evoluționar pentru un anumit număr de generații.
        """
        for generation in range(generations):
            print(f"\nGenerația {generation + 1} - Selecție părinți:")

            # Selectăm perechi de părinți din populația curentă
            children = []
            while len(children) < len(self.population) // 2:  # Generăm population/2 copii în fiecare generație
                parents = self.selection.select_population(2, tsp_data=self.tsp_data)

                # Verificăm dacă părinții sunt liste valide
                if not all(isinstance(parent, list) for parent in parents):
                    raise ValueError(f"Toți părinții trebuie să fie liste valide de orașe. Părinți: {parents}")

                # Aplicăm 2-opt pentru a îmbunătăți soluțiile
                improved_parents = [self.selection.two_opt([parent], self.tsp_data)[0] for parent in parents]

                # Aplicați operatorul de crossover pentru a crea copii din părinți
                new_children = self.crossover.crossover_population(improved_parents)

                # Aplicăm mutația pentru întreaga populație de copii
                mutated_children = self.mutation.mutate_population(new_children)

                # Adăugăm noii copii în lista de copii
                children.extend(mutated_children)

            print(f"Population size: {len(self.population)}")

            # Adăugăm copiii generați în populație
            if len(self.population) + len(children) <= self.max_population_size:
                self.population.extend(children)
            else:
                self.population.sort(key=self.fitness_function)
                best_individual = self.population[0]
                self.population = self.population[1:]
                self.population = self.population[:self.max_population_size - len(children)]
                self.population.extend(children)
                self.population.insert(0, best_individual)

                print(f"Am păstrat cel mai bun individ și am adăugat copiii.")

            # Paralelizăm calculul fitness-ului
            with concurrent.futures.ThreadPoolExecutor() as executor:
                fitness_values = list(executor.map(self.fitness_function, self.population))

            # Salvăm cele mai bune și cele mai slabe trasee
            best_solution = self.population[fitness_values.index(min(fitness_values))]
            worst_solution = self.population[fitness_values.index(max(fitness_values))]
            best_fitness = min(fitness_values)
            worst_fitness = max(fitness_values)

            # Salvăm valorile pentru fiecare generație
            avg_fitness = np.mean(fitness_values)
            self.best_solutions.append(best_fitness)
            self.worst_solutions.append(worst_fitness)
            self.avg_solutions.append(avg_fitness)

            # Salvăm cel mai bun traseu din fiecare generație
            self.best_paths.append(best_solution)

            # Afișăm fitness-ul pentru fiecare generație
            print(
                f"Generația {generation + 1} - Best fitness: {best_fitness}, Worst fitness: {worst_fitness}, Avg fitness: {avg_fitness}")


    def select_best_individuals(self, population, num_best):
        """
        Selectează cei mai buni indivizi pe baza fitness-ului.
        """
        fitness_values = [self.fitness_function(solution) for solution in population]
        sorted_population = [x for _, x in sorted(zip(fitness_values, population), key=lambda pair: pair[0])]
        return sorted_population[:num_best]

    def plot_solutions(self):
        """
        Plotează soluțiile cele mai bune și cele mai slabe pe parcursul generațiilor.
        Reprezentarea va fi similară cu 'plot_solution', dar pentru mai multe soluții.
        """
        # Find the best solution from all generations
        best_solution_index = self.best_solutions.index(min(self.best_solutions))
        best_path = self.best_paths[best_solution_index]  # Get the best path from the best generation
        best_x = [self.tsp_data.get_coordinates()[i][0] for i in best_path]
        best_y = [self.tsp_data.get_coordinates()[i][1] for i in best_path]
        best_x.append(best_x[0])  # return to the starting point
        best_y.append(best_y[0])
        plt.plot(best_x, best_y, 'bo-', markersize=3, label='Best Solution (All Generations)')

        plt.title(f'Best Path (Best Distance: {self.best_solutions[best_solution_index]:.2f})')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.legend(loc='upper right')
        plt.grid(True)
        plt.show()

    def run(self, generations=1000):
        """
        Rulează algoritmul evoluționar.
        """
        print("Începerea evoluției TSP...")
        self.evolve(generations)
        print("Evoluția s-a încheiat.")
        self.plot_solutions()

# Exemplu de utilizare
if __name__ == "__main__":
    tsp_data_file = "ch130.tsp"  # Înlocuiește cu calea fișierului TSP
    main_algorithm = Main(tsp_data_file)
    main_algorithm.run(generations=100)
