import random


class Mutation:
    def __init__(self, mutation_rate=0.1):
        """
        Inițializează clasa pentru mutație.

        :param mutation_rate: Probabilitatea de mutație (implicit 10%).
        """
        self.mutation_rate = mutation_rate

    def mutate(self, solution):
        """
        Aplică Reversal Mutation asupra unei soluții, cu o probabilitate dată.

        :param solution: Soluția curentă (o listă de orașe).
        :return: Soluția modificată, după aplicarea mutației.
        """
        if random.random() < self.mutation_rate:
            # Selectăm două indici aleatori și sortăm pentru a crea un interval valid
            idx1, idx2 = sorted(random.sample(range(len(solution)), 2))
            # Inversăm subsecvența dintre cele două indici
            solution[idx1:idx2 + 1] = reversed(solution[idx1:idx2 + 1])
        return solution
