import random
import math
import concurrent.futures


class Selection:
    def __init__(self, population, fitness_function, tournament_size, coordinates, diversity_penalty_factor=0.9):
        """
        Inițializează clasa de selecție cu mecanism de diversificare.

        :param population: Lista de soluții (indivizi) din populație
        :param fitness_function: Funcția de fitness care calculează valoarea fitness-ului pentru o soluție
        :param tournament_size: Dimensiunea turneului (câte soluții vor participa la selecție)
        :param coordinates: Coordonatele orașelor (lista de perechi x, y)
        :param diversity_penalty_factor: Factorul de penalizare pentru similitudinea între părinți
        """
        self.population = population
        self.fitness_function = fitness_function
        self.tournament_size = tournament_size
        self.coordinates = coordinates  # Lista de coordonate pentru orașe
        self.diversity_penalty_factor = diversity_penalty_factor  # Factorul de penalizare

    def select_parents(self):
        """
        Selectează doi părinți folosind selecția prin turneu și penalizează similitudinea între aceștia.

        :return: 2 părinți selectați din populație
        """
        # Selectăm un turneu de soluții aleatorii
        tournament = random.sample(self.population, self.tournament_size)

        # Sortăm turneul după fitness (mai bine este mai mică distanța pentru TSP)
        tournament_sorted = sorted(tournament, key=self.fitness_function, reverse=False)

        # Selectăm primii doi părinți din turneu
        parent1 = tournament_sorted[0]
        parent2 = tournament_sorted[1]

        # Penalizare pentru similitudinea între părinți
        diversity_penalty = self.calculate_diversity_penalty(parent1, parent2)

        return parent1, parent2

    def calculate_diversity_penalty(self, parent1, parent2):
        """
        Calculează penalizarea pentru similitudinea între doi părinți.

        :param parent1: Primul părinte (traseul 1)
        :param parent2: Al doilea părinte (traseul 2)
        :return: O valoare între 0 și 1, care reprezintă similitudinea între cei doi părinți
        """
        # Măsurăm diferențele între traseele părinților
        difference_count = sum([1 for i in range(len(parent1)) if parent1[i] != parent2[i]])
        return difference_count / len(parent1)

    def select_population(self, num_parents, tsp_data):
        """
        Selectează o populație de părinți pentru încrucișare (poate fi folosită pentru întreaga generație).
        """
        parents = []
        for _ in range(num_parents // 2):  # Selectăm 2 părinți la fiecare iterație
            parent1, parent2 = self.select_parents()

            parents.append(parent1)
            parents.append(parent2)

        return parents

    def two_opt(self, routes, tsp_data):
        """
        Aplica operatorul 2-opt pe multiple trasee simultan folosind paralelism.

        :param routes: Lista de trasee (soluții) ce trebuie îmbunătățite
        :param tsp_data: Obiectul ce conține datele TSP
        :return: Lista de trasee îmbunătățite
        """
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Verifică dacă fiecare traseu din routes este o listă validă
            for route in routes:
                if not isinstance(route, list):
                    raise ValueError(f"Traseul {route} nu este o listă validă de orașe")

            # Trimitem fiecare traseu pentru a fi îmbunătățit
            results = [executor.submit(self.optimize_route, route, tsp_data) for route in routes]

            # Așteptăm ca toate traseele să fie îmbunătățite și returnăm rezultatele
            improved_routes = [future.result() for future in concurrent.futures.as_completed(results)]

        return improved_routes

    def optimize_route(self, route, tsp_data):
        """
        Îmbunătățește un traseu folosind operatorul 2-opt.

        :param route: Traseul curent (lista de orașe)
        :param tsp_data: Obiectul ce conține datele TSP
        :return: Traseul îmbunătățit
        """
        if not isinstance(route, list):
            raise ValueError("Traseul (route) trebuie să fie o listă de orașe")

        best_route = route
        best_distance = self.calculate_total_distance(route)

        # Pre-calculate distances between all cities to avoid redundant calculations
        distance_cache = {}

        def get_distance(i, j):
            """Return cached distance or calculate and store it."""
            if (i, j) not in distance_cache:
                distance_cache[(i, j)] = tsp_data.get_distance(i, j)
            return distance_cache[(i, j)]

        improvement_found = True  # Flag to track improvement

        while improvement_found:
            improvement_found = False  # Reset improvement flag
            for i in range(1, len(route) - 1):
                for j in range(i + 1, len(route)):
                    if j == i + 1:  # Skip adjacent cities (no change possible)
                        continue

                    # Calculate the change in distance caused by the swap
                    prev_city = route[i - 1]
                    city_i = route[i]
                    city_j = route[j]
                    next_city = route[(j + 1) % len(route)]  # Wrap around to the first city

                    old_distance = get_distance(prev_city, city_i) + get_distance(city_j, next_city)
                    new_distance = get_distance(prev_city, city_j) + get_distance(city_i, next_city)

                    delta_distance = new_distance - old_distance

                    # If the new distance is better, apply the swap
                    if delta_distance < 0:
                        route = route[:i] + route[i:j + 1][::-1] + route[j + 1:]
                        best_distance += delta_distance  # Update the best distance incrementally
                        improvement_found = True  # An improvement was found, continue iterating
                        break  # Exit the loop early after finding the first improvement

        return route

    def calculate_total_distance(self, route):
        """
        Calculează distanța totală a unui traseu, având în vedere distanța între fiecare pereche de orașe.

        :param route: Traseul (lista de orașe)
        :return: Distanța totală
        """
        distance = 0
        for i in range(len(route) - 1):
            distance += self.get_distance(route[i], route[i + 1])
        distance += self.get_distance(route[-1], route[0])
        return distance

    def get_distance(self, city1, city2):
        """
        Returnează distanța dintre două orașe utilizând coordonatele lor.

        :param city1: Indexul primului oraș
        :param city2: Indexul celui de-al doilea oraș
        :return: Distanța între cele două orașe
        """
        x1, y1 = self.coordinates[city1]
        x2, y2 = self.coordinates[city2]
        return math.sqrt(((x1 - x2) * (x1 - x2)) + ((y1 - y2) * (y1 - y2)))