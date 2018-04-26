from itertools import chain
from edxDB.df_loader import load_df
from heapq import nlargest
from functools import lru_cache
from edxDB.constants import CONCEPT_EDGES

import time
from typing import List

from .diversified.diversified_results_loader import DiversifiedResultsLoader

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


'''        
def paths_selection(fitness_func, paths: list, top_k=10) -> list():
    if len(paths) < top_k:
        top_k = len(paths)
    fitness = list(map(fitness_func, paths))
    # sort from high to low
    nlargest_indexes = nlargest(top_k, range(len(paths)), key=lambda i: fitness[i])
    # select top k paths
    return [paths[i] for i in nlargest_indexes]
'''
def paths_selection(fitness_func, paths: list, top_k=10) -> list():
    if len(paths) < top_k:
        top_k = len(paths)
    fitness = fitness_func(paths)
    # sort from high to low
    nlargest_indexes = nlargest(top_k, range(len(paths)), key=lambda i: fitness[i])
    # select top k paths
    for i in nlargest_indexes:
        print(fitness[i])
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
        self.relative_score = (mean - self.__score().fillna(0)) / mean


    # === sample of calculate the score of some path ===
    def __score(self):
        return PathEvaluator.student_grade.loc[self.student_id]

    @lru_cache(maxsize=256)
    def __node_position_score(self, position, node, n):
        # parameter B from Wenlong
        # example only
        # implement your own
        return (n - position) * self.relative_score.ix[node]
        
    def evaluate_old(self, path: list) -> float:
        """
        :param path:
        :return: path score
        """
        n = len(path)
        sum_of_product = 0
        for i, node in enumerate(path):
            sum_of_product += self.__node_position_score(i, node, n)
        return sum_of_product
    # === sample ends ===
    
    # === Wenlong's job ===
    def __calc_A(self, path):
        n = len(path)
        score = 0.0
        num_of_failed_descendents = [0] * n
        
        # caculate num_of_failed_descendents[]
        for i in range(n-1,-1,-1):
            for j in range(i+1,n):

                if (path[i] in CONCEPT_EDGES and path[j] in CONCEPT_EDGES[path[i]]):
                    num_of_failed_descendents[i] += 1
                    num_of_failed_descendents[i] += num_of_failed_descendents[j]

        for i in range(n):
            score += 1.0 / (i+1) * num_of_failed_descendents[i]
        
        return score
        
    def __calc_B(self, path):
        n = len(path)
        sum_of_product = 0.0
        
        for i, node in enumerate(path, start = 1):
           sum_of_product += 1.0 / i * self.relative_score.ix[node]
        return sum_of_product
        
    def __calc_C(self, path):
        n = len(path)
        sum_of_product = 0.0
        
        for i in range(0,n):
            for j in range(i+1,n):
                if ((path[i] in self.risk_ratio) and (path[j] in self.risk_ratio[path[i]])):
                    distance = j - i
                    sum_of_product += 1.0 / distance * self.risk_ratio[path[i]][path[j]]
        
        return sum_of_product
        
    def evaluate(self, paths: List[List]):
        # almost the same performance, the easier-to-understand version is chosen
        #raw_scores_A = list(map(self.__calc_A, paths))
        #raw_scores_B = list(map(self.__calc_B, paths))
        #raw_scores_C = list(map(self.__calc_C, paths))
        raw_scores_A = [self.__calc_A(path) for path in paths]
        raw_scores_B = [self.__calc_B(path) for path in paths]
        raw_scores_C = [self.__calc_C(path) for path in paths]
        max_A = max(raw_scores_A)
        max_B = max(raw_scores_B)
        max_C = max(raw_scores_C)
        min_A = min(raw_scores_A)
        min_B = min(raw_scores_B)
        min_C = min(raw_scores_C)
        
        scores = [a + b + c for a, b, c in zip(
          ((a - min_A) / (max_A - min_A) if max_A != min_A else (a - min_A) for a in raw_scores_A),
          ((b - min_B) / (max_B - min_B) if max_B != min_B else (b - min_B) for b in raw_scores_B),
          ((c - min_C) / (max_C - min_C) if max_C != min_C else (c - min_C) for c in raw_scores_C),
        )]

        #scores.append(1.0)
        return scores
    # === Wenlong's job ends === 

# https://stackoverflow.com/questions/279561
def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func

    return decorate


# temporary function to generate paths
# we start with the worst case - all possible paths of topological sort
# estimate all paths and get the top_k paths
#@static_vars(paths=Graph(CONCEPT_EDGES).topological_all())
@static_vars(paths=DiversifiedResultsLoader().load({}))
def generate_paths(student_id, top_k=10):
    evaluator = PathEvaluator(student_id=student_id)
    return paths_selection(evaluator.evaluate, generate_paths.paths, top_k=top_k)


def main():
    # example
    #print(CONCEPT_EDGES)
    start = time.time()
    top_k_paths = generate_paths(student_id=342)
    end = time.time()
    print(top_k_paths)
    running_time = end - start
    print("running time: " + str(running_time))
    #print(CONCEPT_EDGES)


if __name__ == '__main__':
    main()
