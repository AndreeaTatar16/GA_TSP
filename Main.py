import matplotlib.pyplot as plt
import random
import numpy as np

from Mutation import Mutation
from Selection import Selection
from Crossover import Crossover
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
        self.population_size = 10000  # Mărimea populației
        self.population = self.initialize_population()

        # Creăm instanța de selecție
        self.selection = Selection(self.population, self.fitness_function, tournament_size=4)

        # Creăm instanța de crossover
        self.crossover = Crossover()

        # Listă pentru salvarea celor mai bune soluții, soluțiilor medii și celor mai slabe soluții
        self.best_solutions = []
        self.avg_solutions = []
        self.worst_solutions = []

        # Creăm instanța de mutație
        self.mutation = Mutation(mutation_rate=0.5)  # 50% șanse de mutație

    def initialize_population(self):
        """
        Inițializează populația aleatorie de soluții (ordinea orașelor).

        :return: O listă de soluții (populația)
        """
        population = []
        for _ in range(self.population_size):
            # Creăm o soluție randomizată: o permutare aleatorie a orașelor
            solution = list(range(len(self.tsp_data.get_coordinates())))
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

            # Aplicăm mutația pentru fiecare copil
            mutated_children = [self.mutation.mutate(child) for child in children]

            # Afișăm copiii creați și mutați
            print("Copii creați și mutați: ")
            for child in mutated_children:
                print(f"Individ: {child} - Distanță: {self.fitness_function(child)}")

            # Înlocuirea populației cu noii copii
            self.population = mutated_children

            # Calculăm fitness-ul pentru fiecare soluție din populație
            fitness_values = [self.fitness_function(solution) for solution in self.population]

            # Best Solution: Soluția cu cel mai mic fitness (cea mai bună soluție)
            best_solution = self.population[fitness_values.index(min(fitness_values))]
            best_fitness = min(fitness_values)

            # Worst Solution: Soluția cu cel mai mare fitness (cea mai slabă soluție)
            worst_solution = self.population[fitness_values.index(max(fitness_values))]
            worst_fitness = max(fitness_values)

            # Calculăm media fitness-ului (Avg)
            avg_fitness = np.mean(fitness_values)

            # Salvăm valorile pentru fiecare generație
            self.best_solutions.append(best_fitness)
            self.worst_solutions.append(worst_fitness)
            self.avg_solutions.append(avg_fitness)

            # Afișăm fitness-ul pentru fiecare generație (pentru a urmări progresul)
            print(
                f"Generația {generation + 1} - Best fitness: {best_fitness}, Worst fitness: {worst_fitness}, Avg fitness: {avg_fitness}")

    def test_selection(self, selection, num_tests=5000):
        """
        Testează diversitatea selecției prin turneu.
        :param num_tests: Numărul de teste pentru a verifica diversitatea
        """
        selected_parents = []

        for _ in range(num_tests):
            parent1, parent2 = selection.select_parents()
            selected_parents.append((parent1, parent2))

        # Verificăm diversitatea părinților selectați
        similar_pairs = 0
        for i in range(len(selected_parents)):
            for j in range(i + 1, len(selected_parents)):
                if selected_parents[i][0] == selected_parents[j][0] and selected_parents[i][1] == selected_parents[j][
                    1]:
                    similar_pairs += 1

        print(f"Numărul de perechi de părinți similari: {similar_pairs} din {num_tests} selecții")

    def run(self, generations=100):
        """
        Rulează algoritmul evoluționar.

        :param generations: Numărul de generații pentru evoluție
        """

        print("Testare selecție înainte de evoluție:")
        self.test_selection(self.selection)

        print("Începerea evoluției TSP...")
        self.evolve(generations)
        print("Evoluția s-a încheiat.")
        self.plot_solutions(generations)



    def plot_solutions(self, generations):
        """
        Plotează soluțiile cele mai bune, media și cele mai slabe pe parcursul generațiilor.

        :param generations: Numărul de generații
        """
        # Grafic de linii, fără marker-e
        plt.plot(range(generations), self.best_solutions, linestyle='-', color='#5555FF', label='Best Solution')
        #plt.plot(range(generations), self.avg_solutions, linestyle='-', color='b', label='Average Solution')
        plt.plot(range(generations), self.worst_solutions, linestyle='-', color='#FFA500', label='Worst Solution')

        plt.title('Performanța Algoritmului Standard')
        plt.xlabel('Generații')
        plt.ylabel('Fitness Scor')
        plt.legend(loc='upper right')
        plt.grid(True)
        plt.show()


# Exemplu de utilizare
if __name__ == "__main__":
    # Calea către fișierul TSP
    tsp_data_file = "ch130.tsp"  # Înlocuiește cu calea fișierului TSP

    # Inițializăm și rulăm algoritmul
    main_algorithm = Main(tsp_data_file)
    main_algorithm.run(generations=100)
