from scipy.spatial.distance import euclidean

class GTSPProblem:
    def __init__(self, file_path):
        self.coordinates = []
        self.clusters = {}
        self._read_file(file_path)

    def _read_file(self, file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()
            reading_nodes = False
            reading_clusters = False

            for line in lines:
                if "NODE_COORD_SECTION" in line:
                    reading_nodes = True
                    continue
                if "GTSP_SETS" in line:
                    reading_nodes = False
                    reading_clusters = True
                    continue
                if "EOF" in line:
                    break

                if reading_nodes:
                    parts = line.split()
                    self.coordinates.append((float(parts[1]), float(parts[2])))
                if reading_clusters:
                    parts = line.split()
                    cluster_id = int(parts[0])
                    nodes = list(map(int, parts[1:]))
                    self.clusters[cluster_id] = nodes

    def fitness(self, solution):
        total_distance = 0
        prev_node = solution[-1]  # Start from the last node for cyclic tour

        for cluster_id in solution:
            current_node = self.clusters[cluster_id][0]  # Select the first node in the cluster
            total_distance += euclidean(self.coordinates[prev_node - 1], self.coordinates[current_node - 1])
            prev_node = current_node

        return total_distance