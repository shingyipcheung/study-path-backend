import numpy as np
from itertools import combinations
from collections import defaultdict
from numba import jit


@jit(nopython=True)
def displacement(seq1, seq2):
    _sum = 0
    for i in range(len(seq1)):
        _sum += abs(i - seq2.index(seq1[i]))
    return _sum


def feature_distance(seq1, seq2):
    return np.linalg.norm(np.array(seq1) - np.array(seq2))


def order_featrue_transform(possible_sequences):
    ref = possible_sequences[0]
    matrix = np.zeros_like(possible_sequences)
#     list(itertools.permutations(ref, 2))
    for i in range(len(possible_sequences)):
        for j in range(len(ref)):
            matrix[i][j] = possible_sequences[i].index(ref[j])

    return matrix


class Diversifier:

    class Node:
        def __init__(self, idx, seq):
            self.idx = idx
            self.seq = seq
            self.visited = False
            # store the index only
            self.neighbour_dict = defaultdict(list)
            self.degree = 0

        def add_neighbour(self, neighbour, distance):
            self.neighbour_dict[distance].append(neighbour)
            self.degree += 1

        def __str__(self):
            print("index", self.idx)
            print("sequence", self.seq)
            for k, v in self.neighbour_dict.items():
                print("distance to these neighbour", k)
                for neighbour in v:
                    print("\t", neighbour)
            print("degree", self.degree)
            return ""

    @staticmethod
    def build_graph(possible_sequences, distance_func, max_dist):
        graph = [Diversifier.Node(idx, seq) for idx, seq in enumerate(possible_sequences)]
        for v, u in combinations(graph, 2):
            d = distance_func(v.seq, u.seq)
            if d <= max_dist:
                v.add_neighbour(u.idx, d)
                u.add_neighbour(v.idx, d)
        return graph

    @staticmethod
    def diversify_graph(graph):
        # reset graph
        for node in graph:
            node.visited = False

        graph.sort(key=lambda x: x.degree, reverse=True)

        # diversification
        diversified_sequences = []
        for node in graph:
            if not node.visited:
                node.visited = True
                for neighbour_indexes in node.neighbour_dict.values():
                    for neighbour_index in neighbour_indexes:
                        graph[neighbour_index].visited = True
                # for more information
                # diversified_sequences.append(node)
                diversified_sequences.append(node.seq)

        return diversified_sequences
    
    def diversify(self, possible_sequences, distance='displacement', max_dist=16):
        graph = None
        if distance == 'displacement':
            graph = self.build_graph(possible_sequences, displacement, max_dist=max_dist)
        elif distance == 'order_feature':
            matrix = order_featrue_transform(possible_sequences)
            graph = self.build_graph(matrix, feature_distance, max_dist=max_dist)

        return self.diversify_graph(graph), graph
