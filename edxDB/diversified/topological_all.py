from itertools import chain


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


def main():
    from edxDB.constants import CONCEPT_EDGES
    paths = Graph(CONCEPT_EDGES).topological_all()
    print(paths)


if __name__ == "__main__":
    main()
