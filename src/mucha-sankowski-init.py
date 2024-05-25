import numpy as np
from random import randint

class Graph:
    EDGE_EXISTS = 1
    NO_EDGE = 0

    def __init__(self, n):
        self.num_vertices = n
        self.matrix = [[0]*n for i in range(n)]
        
    def add_edge(self, i, j):
        self.matrix[i][j] = self.EDGE_EXISTS
        self.matrix[j][i] = self.EDGE_EXISTS

    def determinant(self, matrix):
        return np.linalg.det(matrix)

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

class TutteGraph(Graph):
    BIG_NUM = 10000

    def __init__(self, n):
        super().__init__(n)

    def add_edge(self, i, j):
        self.matrix[i][j] = self.get_indeterminate(i, j)
        self.matrix[j][i] = self.get_indeterminate(j, i)
    
    def get_indeterminate(self, i, j):
        val = self.BIG_NUM * i + j
        return val if i < j else -val

    def get_val(self, i, j):
        val = abs(self.matrix[i][j])
        if val > 0:
            u = val // self.BIG_NUM
            v = val % self.BIG_NUM
        else:
            u = i
            v = j
            
        if self.matrix[i][j] > 0:
            return "|  X(%2d, %2d)" % (u, v) 
        elif self.matrix[i][j] < 0:
            return "| -X(%2d, %2d)" % (v, u)
        else:
            return "|" + "0".center(11)
        
    def empty_matrix(self):
        n = self.num_vertices
        return [[0] * n for _ in range(n)]

    def get_adj_matrix(self):
        matrix = self.empty_matrix()
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                matrix[i][j] = 1 if self.matrix[i][j] != 0 else 0
        return matrix

    def get_tutte_matrix(self, m=None):
        m = self.num_vertices**2 if m is None else m
        matrix = self.empty_matrix()

        for i in range(len(self.matrix)):
            for j in range(i+1, len(self.matrix[i])):
                if self.matrix[i][j] != 0:
                    random_num = randint(1, m)
                    matrix[i][j] = random_num
                    matrix[j][i] = -random_num
        return matrix

    def rand_has_perfect_matching(self, times=1):
        for _ in range(times):
            result = round(abs(np.linalg.det(self.get_tutte_matrix())), 10) > 0
            if result:
                return True
        return False

    def empty(self, graph_matrix):
        for row in graph_matrix:
            for value in row:
                if value == 1:
                    return False
        return True

    def inverse(self, matrix):
        return np.linalg.inv(matrix)

    def find_next_edge(self, graph_matrix, inv_tutte_matrix):
        for i in range(len(graph_matrix)):
            for j in range(len(graph_matrix[i])):
                if graph_matrix[i][j] == 1 and round(inv_tutte_matrix[i][j], 10) != 0:
                    return (i, j)
        return None

    def delete_edge(self, graph_matrix, edge):
        u, v = edge
        for i in range(len(self.matrix)):
            graph_matrix[u][i] = 0
            graph_matrix[i][u] = 0
            graph_matrix[v][i] = 0
            graph_matrix[i][v] = 0

    def rank(self, matrix):
        return np.linalg.matrix_rank(matrix)

    def eliminate_row_column(self, matrix, row, col):
        n = len(matrix)
        reduced_matrix = np.zeros((n-1, n-1))

        for i in range(n):
            for j in range(n):
                if i != row and j != col:
                    new_i = i - 1 if i > row else i
                    new_j = j - 1 if j > col else j
                    reduced_matrix[new_i][new_j] = matrix[i][j]

        return reduced_matrix

    def get_max_matching(self):
        max_matching = []
        graph_matrix = self.get_adj_matrix()
        print("Rank of the matrix:", self.rank(self.matrix))
        while not self.empty(graph_matrix):
            tutte_matrix = self.get_tutte_matrix()
            try:
                inv_tutte_matrix = self.inverse(tutte_matrix)
            except np.linalg.LinAlgError:
                return "This graph does not have a perfect matching"

            new_edge = self.find_next_edge(graph_matrix, inv_tutte_matrix)
            if new_edge is None:
                break
            i, j = new_edge
                
            max_matching.append(new_edge)
            self.delete_edge(graph_matrix, new_edge)

            tutte_matrix = self.eliminate_row_column(tutte_matrix, i, j)
            inv_tutte_matrix = self.eliminate_row_column(inv_tutte_matrix, i, j)

        return max_matching
    
def main():
    g1 = TutteGraph(3)
    g1.add_edge(0, 1)
    g1.add_edge(0, 2)
    g1.add_edge(1, 2)
    print("G1 have perfect matching?", g1.rand_has_perfect_matching(100))
    print("G1 max matching set:", g1.get_max_matching())

    g2 = TutteGraph(4)
    g2.add_edge(0, 1)
    g2.add_edge(0, 3)
    g2.add_edge(1, 2)
    g2.add_edge(2, 3)
    print("G2 have perfect matching?", g2.rand_has_perfect_matching(100))
    print("G2 max matching set:", g2.get_max_matching())

    g3 = TutteGraph(6)
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
    
    print("G3 have perfect matching?", g3.rand_has_perfect_matching(100))
    print("G3 max matching set:", g3.get_max_matching())

if __name__ == "__main__":
    main()
