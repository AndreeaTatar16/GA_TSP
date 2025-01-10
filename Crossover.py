import random
import concurrent.futures

class Crossover:
    def __init__(self, tsp_data):
        """
        Inițializează operatorul de crossover pentru TSP.

        :param tsp_data: Instanță a clasei TSPData
        """
        self.tsp_data = tsp_data
        self.distance_cache = self._generate_distance_cache()

    def _generate_distance_cache(self):
        """
        Pre-calculăm distanțele între toate orașele pentru a evita calcule repetate.
        """
        distance_cache = {}
        cities = self.tsp_data.get_coordinates()
        for i in range(len(cities)):
            for j in range(i + 1, len(cities)):
                dist = self.tsp_data.get_distance(i, j)
                distance_cache[(i, j)] = dist
                distance_cache[(j, i)] = dist
        return distance_cache

    def select_good_subsequence(self, parent):
        """
        Selectează o sub-secvență bazată pe legături eficiente (distanțe scurte între orașe).

        :param parent: Soluția părinte (lista de orașe)
        :return: Intervalul selectat (start, end)
        """
        size = len(parent)
        best_distance = float('inf')
        best_interval = (0, 0)

        # Iterează prin toate sub-secvențele posibile
        for start in range(size):
            for end in range(start + 1, size):
                # Calculează distanța totală a sub-secvenței folosind cache-ul
                distance = sum(self.distance_cache.get((parent[i], parent[i + 1]), 0) for i in range(start, end))
                if distance < best_distance:
                    best_distance = distance
                    best_interval = (start, end)

        return best_interval

    def order_crossover(self, parent1, parent2):
        """
        Realizează un crossover de tip Order Crossover (OX) între doi părinți, păstrând structurile bune.

        :param parent1: Primul părinte (o listă cu orașe)
        :param parent2: Al doilea părinte (o listă cu orașe)
        :return: O nouă soluție (copil) obținută din cei doi părinți
        """
        size = len(parent1)

        # Selectăm un interval bazat pe distanțele scurte din parent1
        start, end = self.select_good_subsequence(parent1)

        # Creăm o secvență de la primul părinte
        child = [None] * size
        child[start:end + 1] = parent1[start:end + 1]  # Copiem sub-secvența din primul părinte

        # Împlinim restul locațiilor cu orașele care nu sunt deja în subsecvența din child
        current_position = (end + 1) % size
        for city in parent2:
            if city not in child:
                child[current_position] = city
                current_position = (current_position + 1) % size

        return child

    def crossover_population(self, parents, crossover_rate=0.5):
        """
        Realizează crossover asupra întregii populații, garantând că se generează un singur copil pentru fiecare pereche de părinți.

        :param parents: Populația de părinți (lista de soluții)
        :param crossover_rate: Probabilitatea ca un crossover să aibă loc
        :return: O listă de copii generată prin crossover
        """
        children = []
        population_size = len(parents)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for i in range(0, population_size, 2):
                parent1 = parents[i]
                parent2 = parents[(i + 1) % population_size]  # În caz că avem un număr impar de părinți

                # Dacă părintele 1 este identic cu părintele 2, alegem un alt părinte
                if parent1 == parent2:
                    parent2 = parents[(i + 2) % population_size]  # Alegem alt părinte

                # Generăm un copil folosind crossover-ul
                if random.random() < crossover_rate:
                    futures.append(executor.submit(self.order_crossover, parent1, parent2))
                else:
                    futures.append(executor.submit(self.order_crossover, parent1, parent2))

            # Adăugăm copiii în lista finală
            for future in futures:
                children.append(future.result())

        return children
