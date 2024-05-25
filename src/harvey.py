import numpy as np
from random import randint

class Graph:
    EDGE_EXISTS = 1
    NO_EDGE = 0

    def __init__(self, n):
        self.num_vertices = n
        self.matrix = [[0] * n for _ in range(n)]

    def add_edge(self, i, j):
        self.matrix[i][j] = self.EDGE_EXISTS
        self.matrix[j][i] = self.EDGE_EXISTS

    def get_val(self, i, j):
        return "x" if self.matrix[i][j] == self.EDGE_EXISTS else "o"

    def print_graph(self):
        print("  ", end=' ')
        for i in range(len(self.matrix)):
            print(str(i).center(len(self.get_val(i, i))), end=' ')
        print()
        for i in range(len(self.matrix)):
            print(i, end=' ')
            for j in range(len(self.matrix)):
                print(self.get_val(i, j), end=' ')
            print()

class TutteMatrix:
    def __init__(self, graph):
        self.graph = graph
        self.size = graph.num_vertices
        self.matrix = self.construct_tutte_matrix()
        self.inverse = None

    def construct_tutte_matrix(self):
        matrix = np.zeros((self.size, self.size), dtype=float)
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

class HarveyAlgorithm:
    def __init__(self, graph):
        self.graph = graph
        self.tutte_matrix = TutteMatrix(graph)
        self.matching = []

    def construct_perfect_matching(self):
        T = self.tutte_matrix.construct_tutte_matrix()
        self.tutte_matrix.compute_inverse()
        S = list(range(self.graph.num_vertices))
        self.combine_allowed_edges(S)
        return self.matching

    def combine_allowed_edges(self, S):
        if len(S) > 2:
            mid = len(S) // 2
            S1 = S[:mid]
            S2 = S[mid:]
            self.combine_allowed_edges(S1)
            self.combine_allowed_edges(S2)

            for i in S1:
                for j in S2:
                    if self.graph.matrix[i][j] != 0 and round(self.tutte_matrix.inverse[i][j], 10) != 0:
                        if not self.is_in_matching(i) and not self.is_in_matching(j):
                            self.matching.append((i, j))
                            delta = np.zeros_like(self.tutte_matrix.matrix)
                            delta[i, j] = delta[j, i] = self.graph.matrix[i][j]
                            self.graph.matrix[i][j] = self.graph.matrix[j][i] = 0
                            self.tutte_matrix.update_inverse(delta, [i, j])
                            break  
        else:
            if len(S) == 2:
                i, j = S
                if self.graph.matrix[i][j] != 0 and round(self.tutte_matrix.inverse[i][j], 10) != 0:
                    if not self.is_in_matching(i) and not self.is_in_matching(j):
                        self.matching.append((i, j))
                        delta = np.zeros_like(self.tutte_matrix.matrix)
                        delta[i, j] = delta[j, i] = self.graph.matrix[i][j]
                        self.graph.matrix[i][j] = self.graph.matrix[j][i] = 0
                        self.tutte_matrix.update_inverse(delta, [i, j])

    def is_in_matching(self, vertex):
        for u, v in self.matching:
            if u == vertex or v == vertex:
                return True
        return False

def main():
    g1 = Graph(3)
    g1.add_edge(0, 1)
    g1.add_edge(0, 2)
    g1.add_edge(1, 2)
    harvey1 = HarveyAlgorithm(g1)
    print("G1 perfect matching set:", harvey1.construct_perfect_matching())

    g2 = Graph(4)
    g2.add_edge(0, 1)
    g2.add_edge(0, 3)
    g2.add_edge(1, 2)
    g2.add_edge(2, 3)
    harvey2 = HarveyAlgorithm(g2)
    print("G2 perfect matching set:", harvey2.construct_perfect_matching())

    g3 = Graph(6)
    edges = [
        (0, 1), (0, 2), (0, 3), 
        (1, 2), (1, 4),
        (2, 3), (2, 5),
        (3, 4),
        (4, 5),
        (5, 0)
    ]
    for i, j in edges:
        g3.add_edge(i, j)

    harvey3 = HarveyAlgorithm(g3)
    print("G3 perfect matching set:", harvey3.construct_perfect_matching())

if __name__ == "__main__":
    main()
