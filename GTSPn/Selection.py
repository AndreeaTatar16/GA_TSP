import random


class Selection:
    @staticmethod
    def tournament(population, fitnesses, k=3):
        selected = random.sample(list(zip(population, fitnesses)), k)
        return min(selected, key=lambda x: x[1])[0]