import random


class Crossover:
    @staticmethod
    def order_crossover(parent1, parent2):
        size = len(parent1)
        start, end = sorted(random.sample(range(size), 2))

        child = [None] * size
        child[start:end] = parent1[start:end]

        pointer = end
        for gene in parent2:
            if gene not in child:
                if pointer >= size:
                    pointer = 0
                child[pointer] = gene
                pointer += 1

        return child