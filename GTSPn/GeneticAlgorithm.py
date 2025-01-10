import random

from matplotlib import pyplot as plt

from GTSPn.Crossover import Crossover
from GTSPn.GTSPProblem import GTSPProblem
from GTSPn.Mutation import Mutation
from GTSPn.Selection import Selection


class GeneticAlgorithm:
    def __init__(self, problem, pop_size=200, generations=100, mutation_rate=0.2):
        self.problem = problem
        self.pop_size = pop_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.population = []
        self.best_solution = None
        self.best_fitness = float("inf")

    def initialize_population(self):
        num_clusters = len(self.problem.clusters)
        self.population = []
        for _ in range(self.pop_size):
            individual = list(range(1, num_clusters + 1))
            random.shuffle(individual)
            self.population.append(individual)
        print(f"Initialized Population: {len(self.population)} individuals")

    def run(self):
        self.initialize_population()

        for generation in range(self.generations):
            fitnesses = [self.problem.fitness(individual) for individual in self.population]

            if generation == 0:
                print(f"Initial Best Fitness: {min(fitnesses)}")

            for individual, fit in zip(self.population, fitnesses):
                if fit < self.best_fitness:
                    self.best_solution = individual
                    self.best_fitness = fit

            new_population = []
            for _ in range(self.pop_size):
                parent1 = Selection.tournament(self.population, fitnesses)
                parent2 = Selection.tournament(self.population, fitnesses)

                print("\nPărinții selectați pentru crossover:")
                print(f"Parent 1: {parent1}")
                print(f"Parent 2: {parent2}")

                child = Crossover.order_crossover(parent1, parent2)

                print(f"Child generated from crossover: {child}\n")

                Mutation.swap_mutation(child, self.mutation_rate)
                new_population.append(child)

            self.population = new_population

            if generation % 50 == 0 or generation == self.generations - 1:
                print(f"Generation {generation}: Best Fitness = {self.best_fitness}")

        return self.best_solution, self.best_fitness

    def plot_solution(self, solution):
        coordinates = self.problem.coordinates
        clusters = self.problem.clusters

        # Culori pentru clustere
        cluster_colors = plt.cm.get_cmap("tab10", len(clusters))

        plt.figure(figsize=(10, 8))

        for cluster_id, nodes in clusters.items():
            cluster_points = [coordinates[node - 1] for node in nodes]
            x, y = zip(*cluster_points)
            plt.scatter(x, y, color=cluster_colors(cluster_id - 1), label=f"Cluster {cluster_id}")
            for node, (node_x, node_y) in zip(nodes, cluster_points):
                plt.text(node_x, node_y - 0.3, str(node), fontsize=8, ha='center', va='center')

        # Traseu între clustere
        path_points = []
        for cluster_id in solution:
            node = clusters[cluster_id][0]  # Selectăm primul nod din cluster
            path_points.append(coordinates[node - 1])

        # Adăugăm traseul ciclic
        path_points.append(path_points[0])
        x_path, y_path = zip(*path_points)
        plt.plot(x_path, y_path, color="black", linestyle="--", marker="o", label="Path")

        # Adăugăm valoarea soluției în titlu
        fitness_value = self.problem.fitness(solution)
        plt.title(f"GTSP Solution Representation (Best Distance: {fitness_value:.2f})")

        plt.xlabel("X Coordinate")
        plt.ylabel("Y Coordinate")
        plt.legend()
        plt.grid()
        plt.show()


if __name__ == "__main__":
    file_path = "ch130_gtsp.txt"
    problem = GTSPProblem(file_path)

    num_runs = 10
    total_fitness = 0
    best_overall_solution = None
    best_overall_fitness = float("inf")

    for run in range(num_runs):
        print(f"Rulare {run + 1}")
        ga = GeneticAlgorithm(problem, pop_size=100, generations=500, mutation_rate=0.1)
        solution, fitness = ga.run()

        print(f"Rulare {run + 1} - Best Solution: {solution}")
        print(f"Rulare {run + 1} - Fitness: {fitness:.2f}\n")

        total_fitness += fitness

        if fitness < best_overall_fitness:
            best_overall_fitness = fitness
            best_overall_solution = solution

    # Calcularea mediei
    average_fitness = total_fitness / num_runs
    print("\nRezultate finale:")
    print(f"Cea mai bună soluție globală: {best_overall_solution}")
    print(f"Cel mai bun fitness global: {best_overall_fitness:.2f}")
    print(f"Fitness mediu: {average_fitness:.2f}")

    # Reprezentare grafică pentru soluția cea mai bună
    ga.plot_solution(best_overall_solution)