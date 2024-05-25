import numpy as np
from random import randint
from itertools import combinations
import networkx as nx

class Graph:
    def __init__(self, n):
        self.num_vertices = n
        self.matrix = [[0] * n for _ in range(n)]

    def add_edge(self, i, j):
        self.matrix[i][j] = 1
        self.matrix[j][i] = 1

    def remove_edge(self, i, j):
        self.matrix[i][j] = 0
        self.matrix[j][i] = 0

    def get_neighbors(self, v):
        return [i for i in range(self.num_vertices) if self.matrix[v][i] == 1]

    def get_subgraph(self, vertices):
        subgraph = Graph(len(vertices))
        index_map = {v: i for i, v in enumerate(vertices)}
        for i in range(len(vertices)):
            for j in range(len(vertices)):
                if self.matrix[vertices[i]][vertices[j]] == 1:
                    subgraph.add_edge(i, j)
        return subgraph, index_map

    def to_networkx(self):
        g = nx.Graph()
        for i in range(self.num_vertices):
            for j in range(i + 1, self.num_vertices):
                if self.matrix[i][j] == 1:
                    g.add_edge(i, j)
        return g

class TutteMatrix:
    def __init__(self, graph):
        self.graph = graph
        self.size = graph.num_vertices
        self.matrix = self.construct_tutte_matrix()
        self.inverse = None

    def construct_tutte_matrix(self):
        matrix = np.zeros((self.size, self.size), dtype=int)
        for i in range(self.size):
            for j in range(i + 1, self.size):
                if self.graph.matrix[i][j] != 0:
                    sign = 1 if i < j else -1
                    matrix[i][j] = sign * (self.size * i + j)
                    matrix[j][i] = -matrix[i][j]
        return matrix

    def instantiate(self):
        instantiated_matrix = np.zeros((self.size, self.size), dtype=float)
        for i in range(self.size):
            for j in range(self.size):
                if self.matrix[i][j] != 0:
                    instantiated_matrix[i][j] = randint(1, self.size ** 2)
                else:
                    instantiated_matrix[i][j] = 0
        return instantiated_matrix

    def compute_inverse(self):
        retry_limit = 10
        for attempt in range(retry_limit):
            try:
                instantiated_matrix = self.instantiate()
                self.inverse = np.linalg.inv(instantiated_matrix)
                print(f"Inverse computed on attempt {attempt + 1}")
                return self.inverse
            except np.linalg.LinAlgError:
                print(f"Singular matrix encountered on attempt {attempt + 1}")
                continue
        raise np.linalg.LinAlgError("Unable to compute non-singular inverse after several attempts")

    def update_inverse(self, delta, subset):
        U = delta[:, subset]
        V = delta[subset, :]
        C = self.inverse[subset, :]
        D = self.inverse[:, subset]
        I = np.eye(len(subset))

        if np.linalg.det(I + np.dot(np.dot(V, self.inverse), U)) != 0:
            self.inverse -= np.dot(np.dot(self.inverse, U), np.linalg.inv(I + np.dot(np.dot(V, self.inverse), U))) @ np.dot(V, self.inverse)
        else:
            raise np.linalg.LinAlgError("Update resulted in singular matrix")

class MatchingAlgorithm:
    def __init__(self, graph):
        self.graph = graph
        self.k = 1
        self.matching = []

    def find_maximum_matching(self):
        while self.k <= self.graph.num_vertices:
            try:
                S, C_components = self.find_k_separator(self.k)
                T = TutteMatrix(self.graph).construct_tutte_matrix()

                for C in C_components:
                    subgraph, index_map = self.graph.get_subgraph(C)
                    tutte_matrix = TutteMatrix(subgraph)
                    tutte_matrix.compute_inverse()

                    self.combine_allowed_edges(tutte_matrix, C, index_map)

                return self.matching

            except (ValueError, np.linalg.LinAlgError) as e:
                print(f"Error encountered for k={self.k}: {e}")
                self.k += 1

        raise ValueError("No valid k-separator found for any k up to the number of vertices")

    def find_k_separator(self, k):
        g = self.graph.to_networkx()
        for size in range(1, k + 1):
            for S in combinations(range(self.graph.num_vertices), size):
                remaining_vertices = set(range(self.graph.num_vertices)) - set(S)
                subgraph = g.subgraph(remaining_vertices)
                components = list(nx.connected_components(subgraph))
                if all(len(comp) <= k - len(S) for comp in components):
                    return list(S), [list(comp) for comp in components]
        raise ValueError("No valid k-separator found")

    def combine_allowed_edges(self, tutte_matrix, C, index_map):
        for i in range(len(C)):
            for j in range(i + 1, len(C)):
                if tutte_matrix.matrix[i][j] != 0 and round(tutte_matrix.inverse[i][j], 10) != 0:
                    if not self.is_in_matching(C[i]) and not self.is_in_matching(C[j]):
                        self.matching.append((C[i], C[j]))
                        delta = np.zeros_like(tutte_matrix.matrix)
                        delta[i, j] = delta[j, i] = tutte_matrix.matrix[i][j]
                        tutte_matrix.matrix[i][j] = tutte_matrix.matrix[j][i] = 0
                        try:
                            tutte_matrix.update_inverse(delta, [i, j])
                        except np.linalg.LinAlgError:
                            print(f"Failed to update inverse for edge ({C[i]}, {C[j]})")

    def is_in_matching(self, vertex):
        for u, v in self.matching:
            if u == vertex or v == vertex:
                return True
        return False

def main():
    g = Graph(10)
    edges = [
        (0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6), 
        (3, 7), (4, 8), (5, 9), (6, 9), (7, 8), (8, 9),
        (0, 3), (1, 5), (2, 4), (3, 6), (4, 7), (5, 8)
    ]
    for i, j in edges:
        g.add_edge(i, j)

    matching_algorithm = MatchingAlgorithm(g)
    try:
        matching = matching_algorithm.find_maximum_matching()
        print("Maximum matching:", matching)
    except ValueError as e:
        print(str(e))

if __name__ == "__main__":
    main()
