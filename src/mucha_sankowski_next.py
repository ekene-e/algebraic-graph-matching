import numpy as np
from random import randint

class BipartiteGraph:
    def __init__(self, n):
        self.num_vertices = n
        self.matrix = [[0] * n for _ in range(n)]
        
    def add_edge(self, i, j):
        self.matrix[i][j] = 1
        self.matrix[j][i] = 1

    def get_indeterminate(self, i, j):
        return 'x_{}_{}'.format(i, j)

    def get_val(self, i, j):
        return self.matrix[i][j]

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

class EdmondsMatrix:
    def __init__(self, graph):
        self.graph = graph
        self.size = graph.num_vertices
        self.matrix = self.construct_matrix()
        self.inverse = None

    def construct_matrix(self):
        matrix = np.zeros((self.size, self.size), dtype=object)
        for i in range(self.size):
            for j in range(self.size):
                if self.graph.matrix[i][j] != 0:
                    matrix[i][j] = self.graph.get_indeterminate(i, j)
                else:
                    matrix[i][j] = 0
        return matrix

    def instantiate(self):
        instantiated_matrix = np.zeros((self.size, self.size), dtype=float)
        for i in range(self.size):
            for j in range(self.size):
                if self.matrix[i][j] != 0:
                    instantiated_matrix[i][j] = randint(1, 1000)
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

    def update_inverse(self, row, col):
        if self.inverse is None:
            self.compute_inverse()
        u = self.inverse[:, col]
        v = self.inverse[row, :]
        c = self.inverse[row, col]
        if np.abs(c) > 1e-10:
            self.inverse = self.inverse - np.outer(u, v) / c
        else:
            print(f"Warning: Small or zero pivot encountered at row {row}, col {col}, skipping update")

class MuchaSankowski:
    def __init__(self, graph):
        self.graph = graph
        self.edmonds_matrix = EdmondsMatrix(graph)
        self.matching = []

    def match(self, p, q):
        if p == q:
            for r in range(self.graph.num_vertices):
                if self.graph.matrix[p][r] != 0 and round(self.edmonds_matrix.inverse[r, p], 10) != 0:
                    self.matching.append((p, r))
                    self.graph.matrix[p][r] = 0
                    self.graph.matrix[r][p] = 0
                    self.edmonds_matrix.update_inverse(p, r)
                    break
        else:
            m = (p + q) // 2
            self.match(p, m)
            self.match(m + 1, q)
            self.update_uneliminated_rows(p, q)

    def update_uneliminated_rows(self, start, end):
        for i in range(start, end + 1):
            for j in range(self.graph.num_vertices):
                if self.graph.matrix[i][j] != 0 and round(self.edmonds_matrix.inverse[i][j], 10) != 0:
                    self.graph.matrix[i][j] = 0
                    self.graph.matrix[j][i] = 0

    def get_max_matching(self):
        self.edmonds_matrix.compute_inverse()
        self.match(0, self.graph.num_vertices - 1)
        return self.matching

def main():
    g1 = BipartiteGraph(3)
    g1.add_edge(0, 1)
    g1.add_edge(0, 2)
    g1.add_edge(1, 2)
    ms1 = MuchaSankowski(g1)
    print("G1 max matching set:", ms1.get_max_matching())

    g2 = BipartiteGraph(4)
    g2.add_edge(0, 1)
    g2.add_edge(0, 3)
    g2.add_edge(1, 2)
    g2.add_edge(2, 3)
    ms2 = MuchaSankowski(g2)
    print("G2 max matching set:", ms2.get_max_matching())

    g3 = BipartiteGraph(6)
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
    
    ms3 = MuchaSankowski(g3)
    print("G3 max matching set:", ms3.get_max_matching())

if __name__ == "__main__":
    main()
