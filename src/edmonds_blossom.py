class Graph:
    def __init__(self):
        self.adjacency = {}
        self.unmarked_adjacency = {}
    
    def add_edge(self, u, v):
        if u not in self.adjacency:
            self.adjacency[u] = set()
            self.unmarked_adjacency[u] = set()
        if v not in self.adjacency:
            self.adjacency[v] = set()
            self.unmarked_adjacency[v] = set()
        self.adjacency[u].add(v)
        self.adjacency[v].add(u)
        self.unmarked_adjacency[u].add(v)
        self.unmarked_adjacency[v].add(u)
    
    def unmark_all_edges(self):
        self.unmarked_adjacency = {u: set(neighbors) for u, neighbors in self.adjacency.items()}
    
    def mark_edge(self, u, v):
        self.unmarked_adjacency[u].discard(v)
        self.unmarked_adjacency[v].discard(u)
    
    def get_unmarked_neighboring_edge(self, u):
        if u in self.unmarked_adjacency and self.unmarked_adjacency[u]:
            return (u, next(iter(self.unmarked_adjacency[u])))
        return None

    def contract(self, blossom):
        new_graph = Graph()
        new_vertex = blossom.id
        new_graph.adjacency[new_vertex] = set()
        for v in blossom.vertices:
            for u in self.adjacency[v]:
                if u not in blossom.vertices:
                    new_graph.add_edge(new_vertex, u)
        for v in self.adjacency:
            if v not in blossom.vertices:
                new_graph.adjacency[v] = set(self.adjacency[v])
        new_graph.unmark_all_edges()
        return new_graph
    
    def lift_path(self, path, blossom):
        if not path:
            return path
        if len(path) == 1:
            raise ValueError("A path cannot contain exactly one vertex")

        def find_path_through_blossom(endpoint):
            for direction in [blossom.traverse_left, blossom.traverse_right]:
                blossom_path = list(direction())
                for i, v in enumerate(blossom_path):
                    if endpoint in self.adjacency[v]:
                        if i % 2 == 0:
                            return blossom_path[:i + 1]
                        else:
                            return list(reversed(blossom_path[:i + 1]))
            raise ValueError("A valid path through the blossom was not found")

        expanded_path = []
        for i, v in enumerate(path):
            if v == blossom.id:
                if i == 0:
                    expanded_path.extend(find_path_through_blossom(path[i + 1]))
                elif i == len(path) - 1:
                    expanded_path.extend(reversed(find_path_through_blossom(path[i - 1])))
                else:
                    expanded_path.extend(reversed(find_path_through_blossom(path[i - 1])))
                    expanded_path.pop()
                    expanded_path.extend(find_path_through_blossom(path[i + 1]))
            else:
                expanded_path.append(v)
        return expanded_path


class Matching:
    def __init__(self):
        self.adjacency = {}
        self.edges = set()
        self.exposed_vertices = set()
    
    def add_vertex(self, v):
        if v not in self.adjacency:
            self.adjacency[v] = set()
            self.exposed_vertices.add(v)
    
    def add_edge(self, u, v):
        if u not in self.adjacency:
            self.add_vertex(u)
        if v not in self.adjacency:
            self.add_vertex(v)
        self.adjacency[u].add(v)
        self.adjacency[v].add(u)
        self.edges.add((u, v))
        self.exposed_vertices.discard(u)
        self.exposed_vertices.discard(v)
    
    def augment(self, path):
        for i in range(0, len(path) - 1, 2):
            self.add_edge(path[i], path[i + 1])
        return self
    
    def get_edges(self):
        return self.edges
    
    def get_exposed_vertices(self):
        return self.exposed_vertices
    
    def get_matched_vertex(self, v):
        return next(iter(self.adjacency[v]))


class Blossom:
    count = 0
    
    def __init__(self, vertices, base):
        Blossom.count += 1
        self.id = -Blossom.count
        self.vertices = vertices
        self.base = base
    
    def traverse_left(self):
        yield from self.vertices
    
    def traverse_right(self):
        yield from reversed(self.vertices)


class Forest:
    def __init__(self):
        self.roots = {}
        self.distances_to_root = {}
        self.unmarked_even_vertices = set()
        self.parents = {}
    
    def add_singleton_tree(self, v):
        self.roots[v] = v
        self.distances_to_root[v] = 0
        self.unmarked_even_vertices.add(v)
        self.parents[v] = v
    
    def get_unmarked_even_vertex(self):
        if self.unmarked_even_vertices:
            return next(iter(self.unmarked_even_vertices))
        return None
    
    def mark_vertex(self, v):
        if self.distances_to_root[v] % 2 == 0:
            self.unmarked_even_vertices.discard(v)
    
    def contains_vertex(self, v):
        return v in self.roots
    
    def add_edge(self, u, v):
        if u not in self.roots:
            self.roots[u] = self.roots[v]
            self.distances_to_root[u] = self.distances_to_root[v] + 1
            if self.distances_to_root[u] % 2 == 0:
                self.unmarked_even_vertices.add(u)
            self.parents[u] = v
        elif v not in self.roots:
            self.roots[v] = self.roots[u]
            self.distances_to_root[v] = self.distances_to_root[u] + 1
            if self.distances_to_root[v] % 2 == 0:
                self.unmarked_even_vertices.add(v)
            self.parents[v] = u
    
    def get_distance_to_root(self, v):
        return self.distances_to_root[v]
    
    def get_root(self, v):
        return self.roots[v]
    
    def get_path_from_root_to(self, v):
        path = []
        while self.parents[v] != v:
            path.append(v)
            v = self.parents[v]
        path.append(v)
        return path
    
    def get_blossom(self, v, w):
        v_path = self.get_path_from_root_to(v)
        w_path = self.get_path_from_root_to(w)
        common_ancestor = next(u for u in v_path if u in w_path)
        blossom_vertices = v_path[:v_path.index(common_ancestor)] + w_path[w_path.index(common_ancestor)::-1]
        return Blossom(blossom_vertices, common_ancestor)


def get_augmenting_path(graph, matching):
    forest = Forest()
    graph.unmark_all_edges()
    for v in matching.get_exposed_vertices():
        forest.add_singleton_tree(v)
    
    v = forest.get_unmarked_even_vertex()
    while v is not None:
        e = graph.get_unmarked_neighboring_edge(v)
        while e is not None:
            _, w = e
            if not forest.contains_vertex(w):
                x = matching.get_matched_vertex(w)
                forest.add_edge(v, w)
                forest.add_edge(w, x)
            else:
                if forest.get_distance_to_root(w) % 2 == 0:
                    if forest.get_root(v) != forest.get_root(w):
                        return forest.get_path_from_root_to(v) + forest.get_path_from_root_to(w)[::-1]
                    else:
                        blossom = forest.get_blossom(v, w)
                        graph_prime = graph.contract(blossom)
                        matching_prime = matching.contract(blossom)
                        path_prime = get_augmenting_path(graph_prime, matching_prime)
                        return graph.lift_path(path_prime, blossom)
            graph.mark_edge(*e)
            e = graph.get_unmarked_neighboring_edge(v)
        forest.mark_vertex(v)
        v = forest.get_unmarked_even_vertex()
    return []


def get_maximum_matching(graph, matching):
    augmenting_path = get_augmenting_path(graph, matching)
    if augmenting_path:
        matching.augment(augmenting_path)
        return get_maximum_matching(graph, matching)
    return matching

def test_case_1():
    graph = Graph()
    graph.add_edge(1, 2)
    graph.add_edge(3, 4)

    matching = Matching()
    matching.add_vertex(1)
    matching.add_vertex(2)
    matching.add_vertex(3)
    matching.add_vertex(4)

    maximum_matching = get_maximum_matching(graph, matching)
    print("Test case: simple graph")
    print("-" * len("Test case: simple graph"))
    print("Edges in maximum matching:", maximum_matching.get_edges())
    print("\n")

def test_case_2():
    graph = Graph()
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)
    graph.add_edge(4, 5)
    graph.add_edge(5, 6)
    graph.add_edge(6, 1)

    matching = Matching()
    matching.add_vertex(1)
    matching.add_vertex(2)
    matching.add_vertex(3)
    matching.add_vertex(4)
    matching.add_vertex(5)
    matching.add_vertex(6)

    maximum_matching = get_maximum_matching(graph, matching)
    print("Test case: graph with odd cycle")
    print("-" * len("Test case: graph with odd cycle"))
    print("Edges in maximum matching:", maximum_matching.get_edges())
    print("\n")

def test_case_3():
    graph = Graph()
    graph.add_edge(1, 2)
    graph.add_edge(1, 3)
    graph.add_edge(2, 4)
    graph.add_edge(3, 4)
    graph.add_edge(4, 5)
    graph.add_edge(5, 8)
    graph.add_edge(6, 7)
    graph.add_edge(7, 8)
    graph.add_edge(3, 6)

    matching = Matching()
    matching.add_vertex(1)
    matching.add_vertex(2)
    matching.add_vertex(3)
    matching.add_vertex(4)
    matching.add_vertex(5)
    matching.add_vertex(6)
    matching.add_vertex(7)
    matching.add_vertex(8)

    maximum_matching = get_maximum_matching(graph, matching)
    print("Test case: small but slightly bigger graph")
    print("-" * len("Test case: small but slightly bigger graph"))
    print("Edges in maximum matching:", maximum_matching.get_edges())
    print("\n")

def test_case_4():
    graph = Graph()
    graph.add_edge(1, 2)
    graph.add_edge(3, 4)

    matching = Matching()
    matching.add_vertex(1)
    matching.add_vertex(2)
    matching.add_vertex(3)
    matching.add_vertex(4)

    maximum_matching = get_maximum_matching(graph, matching)
    print("Test case: disconnected graph")
    print("-" * len("Test case: disconnected graph"))
    print("Edges in maximum matching:", maximum_matching.get_edges())
    print("\n")

print("\n")
test_case_1()
test_case_2()
test_case_3()
test_case_4()