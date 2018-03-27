# permutation example by Luc

def find_node_set(dictionary):
    '''
    **goal**: find the set of:
              1. all nodes
              2. all nodes that is some others' parent
              3. all nodes that is some others' child
    :param dictionary: dictionary of edges, parent -> list of children
    '''
    from itertools import chain
    all_parents = set(dictionary.keys())
    all_children = set(chain(*[v for v in dictionary.values()]))
    all_nodes = all_parents | all_children
    return all_nodes, all_parents, all_children

def create_dependency_map_with_index(dictionary, all_nodes):
    '''
    **goal**: convert nodes with string names into integer indices

    :param dictionary: dictionary of edges, parent -> list of children
    :param all_nodes: set of all nodes
    '''
    node_cnt = len(all_nodes)
    import numpy as np
    node2ind = {n: i for i, n in enumerate(all_nodes)}
    indmap = np.zeros((node_cnt, node_cnt))
    # map: row=parent, col=child
    for p in all_nodes:
        if p in dictionary:
            for c in dictionary[p]:
                indmap[node2ind[p], node2ind[c]] = 1
    return node2ind, indmap


# === brutal pruning ===
def permutation(all_nodes:set, node2ind, indmap):
    visited = []
    unvisited = set((node2ind[n] for n in all_nodes)) # create set of unvisited indices
    all_possible = []

    def _step():
        nonlocal unvisited, visited, all_possible, indmap
        if not unvisited:
            # if unvisited is empty, then this is a legal permutation
            all_possible.append(tuple(visited))
            return
        for i in unvisited:
            # check if valid
            for j in visited:
                # if j->i, i.e. indmap[j,i] != 0, then illegal
                if indmap[j,i] != 0:
                    return
            # put into visited, visit next position
            visited.append(i)
            unvisited.remove(i)
            _step()
            # remove from visited
            del visited[-1]
            unvisited.add(i)

    _step()

    return all_possible



CONCEPT_EDGES = {
    "primitive_type": ["operator", "array", "variable"],
    "operator": ["branch"],
    "branch": ["loop"],
    "array": ["nd_array", "string"],
    "variable": ["array", "instance_variable"],
    "object_class": ["instance_variable", "method"],
    "instance_variable": ["method"],
    "method": ["recursion"]
}

all_nodes, all_parents, all_children = find_node_set(CONCEPT_EDGES)
node_cnt = len(all_nodes)

node2ind, indmap = create_dependency_map_with_index(CONCEPT_EDGES, all_nodes)

ret = permutation(all_nodes, node2ind, indmap)

print(len(ret))
