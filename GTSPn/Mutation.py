import random


class Mutation:
    @staticmethod
    def swap_mutation(individual, mutation_rate):
        for i in range(len(individual)):
            if random.random() < mutation_rate:
                swap_idx = random.randint(0, len(individual) - 1)
                individual[i], individual[swap_idx] = individual[swap_idx], individual[i]