import numpy as np
import itertools
from collections import defaultdict
import datetime
import math
import random


'''
Usage of Diversifier
Diversifier.diversify(seq)
Diversifier.diversify_graph(graph)
'''

class Diviersifier():
    #Node
    class Node:
        def __init__(self, name, seq):
            self.id = name
            self.seq = seq
            self.visited = False
            self.neighbour = defaultdict(list)
            self.degree = 0
            
    def displacement(self, seq1, seq2):
        sum = 0
        for i in range(len(seq1)):
            s = i - seq2.index(seq1[i])
            sum += abs(s)
        return sum
    
    def feature_distance(self, seq1, seq2):
        return np.linalg.norm(np.array(seq1)-np.array(seq2))  
    
    def order_featrue_transform(self, possible_sequences):
        ref = possible_sequences[0]
        M = np.zeros_like(possible_sequences)
    #     list(itertools.permutations(ref, 2))
        for i in range(len(possible_sequences)):
            for j in range(len(ref)):
                M[i][j] = possible_sequences[i].index(ref[j])

        return M
    
    def build_graph(self, possible_sequences, distance, max_dist):
       # print('Building Graph ...\n')
        #a = datetime.datetime.now()
        G = []
        for i in range(len(possible_sequences)):
            cur = self.Node(i, possible_sequences[i])
            for j in range(len(possible_sequences)):
                s = distance(cur.seq, possible_sequences[j])
                if s <= max_dist:
                    cur.neighbour[s].append(j)
                    cur.degree += 1
            G.append(cur)
       # b = datetime.datetime.now()
        #print('time elapsed:' + str(b-a) + '\n')
        return G 
    
    def diversify_graph(self, G, possible_sequences, r):
        #Reset graph 
        for node in G:
            node.visited = False

        G.sort(key=lambda x: x.degree, reverse=True)

        #Diversification
        Q = []
        for node in G:
            neighbour = []
            if node.visited == False:
                node.visited = True
                for key in node.neighbour.keys():
                    if key <= r:
                        neighbour += node.neighbour[key]
                for n in neighbour:
                    G[n].visited = True
                Q.append(node)
                
        R = []
        for i in Q:
            R.append(possible_sequences[i.id])
        
        return R
    
    def diversify(self, possible_sequences, distance='displacement', r=16):
        if distance == 'displacement':
            graph = self.build_graph(possible_sequences, self.displacement, 20)
        elif distance == 'order_feature':
            M = self.order_featrue_transform(possible_sequences)
            graph = self.build_graph(M, self.feature_distance)
        
        return graph, self.diversify_graph(graph, possible_sequences, r)


