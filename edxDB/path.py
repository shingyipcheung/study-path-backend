from itertools import chain
from edxDB.df_loader import load_df
from heapq import nlargest
from functools import lru_cache


def generate_ratio_dict():
    risk_ratio = load_df("risk_ratio.pkl")
    ratio_dict = {}
    for index, row in risk_ratio.iterrows():
        v, u, w = row["source"], row["target"], row["value"]
        if v in ratio_dict:
            ratio_dict[v][u] = w
        else:
            ratio_dict[v] = {u: w}
    return ratio_dict


class Graph:
    def __init__(self, edges):
        self.edges = edges
        self.all_nodes = set(edges.keys()) | set(self.all_children(edges))
        # init all indegree
        self.indegree = {key: 0 for key in self.all_nodes}
        for v in self.all_children(edges):
            self.indegree[v] += 1

    @staticmethod
    def all_children(edges):
        return chain.from_iterable([v for v in edges.values()])

    @staticmethod
    def breath_first_search(edges):
        # BFS for Disconnected Graph
        if len(edges) == 0:
            return []
        from collections import deque

        visited = set()
        path = list()

        for node in edges.keys():
            queue = deque()
            queue.append(node)
            if node not in visited:
                visited.add(node)
                while len(queue) != 0:
                    v = queue.popleft()
                    path.append(v)
                    if v in edges:
                        for u in edges[v]:
                            if u not in visited:
                                visited.add(u)
                                queue.append(u)
        return path

    def topological_all(self):
        """
        # https://www.geeksforgeeks.org/all-topological-sorts-of-a-directed-acyclic-graph/
        # :param edges: adjacency list of graph representation
        :return: a list of lists: all possible paths
        """
        unvisited = self.all_nodes.copy()
        paths = []
        path = []

        def topological_recursive():
            if not unvisited:
                paths.append(path.copy())
            else:
                for node in self.all_nodes:
                    if node in unvisited and self.indegree[node] == 0:
                        if node in self.edges:
                            for child in self.edges[node]:
                                self.indegree[child] -= 1
                        path.append(node)
                        unvisited.remove(node)

                        topological_recursive()

                        path.pop()
                        unvisited.add(node)
                        if node in self.edges:
                            for child in self.edges[node]:
                                self.indegree[child] += 1

        topological_recursive()
        return paths


def paths_selection(fitness_func, paths: list, top_k=10) -> list():
    if len(paths) < top_k:
        top_k = len(paths)
    fitness = list(map(fitness_func, paths))
    # sort from high to low
    nlargest_indexes = nlargest(top_k, range(len(paths)), key=lambda i: fitness[i])
    # select top k paths
    return [paths[i] for i in nlargest_indexes]


class PathEvaluator:
    # static variable for calculation
    risk_ratio = generate_ratio_dict()
    mean = load_df("concept_score_mean.pkl")
    student_grade = load_df("student_concept_grade.pkl")

    def __init__(self, student_id):
        self.student_id = student_id
        mean = PathEvaluator.mean
        # diff between student score and mean
        self.relative_score = (mean - self.score().fillna(0)) / mean

    def score(self):
        return PathEvaluator.student_grade.loc[self.student_id]

    @lru_cache(maxsize=256)
    def node_position_score(self, position, node, n):
        # parameter B from Wenlong
        return (n - position) * self.relative_score.ix[node]

    def evaluate(self, path: list) -> float:
        """
        :param path:
        :return: path score
        """
        n = len(path)
        sum_of_product = 0
        for i, node in enumerate(path):
            sum_of_product += self.node_position_score(i, node, n)
        return sum_of_product


def main():
    from edxDB.constants import CONCEPT_EDGES
    graph = Graph(CONCEPT_EDGES)
    paths = graph.topological_all()
    evaluator = PathEvaluator(student_id=69845)
    top_k_paths = paths_selection(evaluator.evaluate, paths, top_k=5)
    print(top_k_paths)


if __name__ == '__main__':
    main()
