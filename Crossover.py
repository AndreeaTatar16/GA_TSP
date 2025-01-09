import random


class Crossover:
    def __init__(self):
        """
        Inițializează operatorul de crossover pentru TSP.
        """
        pass

    def order_crossover(self, parent1, parent2):
        """
        Realizează un crossover de tip Order Crossover (OX) între două soluții parentale.

        :param parent1: Primul părinte (o listă cu orașe)
        :param parent2: Al doilea părinte (o listă cu orașe)
        :return: O nouă soluție (copil) obținută din cei doi părinți
        """
        size = len(parent1)

        # Alege un interval aleator pentru a selecta subsecvența din primul părinte
        start, end = sorted(random.sample(range(size), 2))

        # Creăm o secvență de la primul părinte
        child = [None] * size
        child[start:end + 1] = parent1[start:end + 1]  # Copiem subsecvența din primul părinte

        # Împlinim restul locațiilor cu orașele care nu sunt deja în subsecvența din child
        current_position = (end + 1) % size
        for city in parent2:
            if city not in child:
                child[current_position] = city
                current_position = (current_position + 1) % size

        return child

    def crossover_population(self, parents, crossover_rate=0.8):
        """
        Realizează crossover asupra întregii populații.

        :param parents: Populația de părinți (lista de soluții)
        :param crossover_rate: Probabilitatea ca un crossover să aibă loc
        :return: O listă de copii generată prin crossover
        """
        children = []
        population_size = len(parents)

        for i in range(0, population_size, 2):
            parent1 = parents[i]
            parent2 = parents[(i + 1) % population_size]  # În caz că avem un număr impar de părinți

            if random.random() < crossover_rate:
                child = self.order_crossover(parent1, parent2)
                children.append(child)
            else:
                # Fără crossover, copiem părintele direct
                children.append(parent1)
                children.append(parent2)

        return children
