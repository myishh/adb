import snap
import numpy as np
import matplotlib.pyplot as plt
import copy
import random

def GetNeighbors(Graph, NodeId):
    NI = Graph.GetNI(NodeId)
    d = NI.GetDeg()
    neighbors = []
    for i in xrange(d):
        neighbors.append(NI.GetNbrNId(i))
    return neighbors

def SortedPair(a, b):
    small  = min(a, b)
    big = max(a, b)
    return (small, big)

def Tree(G, start):
    relatives = [{"p":set(), "c":set()} for i in xrange(G.GetNodes())]
    parents = [start]
    children = set()
    checked = set(parents)
    while len(checked) < G.GetNodes():
        while parents:
            p = parents.pop()
            nbrs = GetNeighbors(G, p)
            for nbr in nbrs:
                if nbr not in checked:
                    relatives[p]["c"].add(nbr)
                    relatives[nbr]["p"].add(p)
                    children.add(nbr)

        parents = list(children)
        checked = checked.union(children)
        children = set()
    return relatives

numNodes = 1000
G = snap.GenPrefAttach(numNodes, 4)

edgeList = []
for edge in G.Edges():
    a = edge.GetSrcNId()
    b = edge.GetDstNId()
    edgeList.append(SortedPair(a, b))

# Algorithm 1
between = {e:0.0 for e in edgeList}
for i in xrange(numNodes):
    relatives = Tree(G, i)
    sigmas = [0.0] * numNodes
    sigmas[i] = 1.0
    parents = [i]
    children = set()
    checked = set(parents)
    layers = [set(parents)]
    while len(checked) < numNodes:
        while parents:
            p = parents.pop()
            children = children.union(relatives[p]['c'])
        for c in children:
            sigmas[c] = sum([sigmas[k] for k in relatives[c]["p"]])
        checked = checked.union(children)
        parents = children
        layers.append(copy.copy(children))
        children = set()
    flow = [1.0] * numNodes
    children = set()
    for i in xrange(numNodes):
        if not relatives[i]['c']:
            children.add(i)
    parents = set()
    checked = children
    while layers:
        layer = list(layers.pop())
        while layer:
            c = layer.pop()
            ancestors = relatives[c]['p']
            for k in ancestors:
                newflow = flow[c] * sigmas[k] / sigmas[c]
                between[SortedPair(c, k)] += newflow
                flow[k] += newflow

# Algorithm 2
betweenAppr = {e:0.0 for e in edgeList}
betweenK = {e:0 for e in edgeList}
for s in xrange(numNodes / 10):
    if sum(np.array(betweenAppr.values()) <= 5 * numNodes) == 0:
        break
    i = random.sample(xrange(numNodes), 1)[0]
    relatives = Tree(G, i)
    sigmas = [0.0] * numNodes
    sigmas[i] = 1.0
    parents = [i]
    children = set()
    checked = set(parents)
    layers = [set(parents)]
    while len(checked) < numNodes:
        while parents:
            p = parents.pop()
            children = children.union(relatives[p]['c'])
        for c in children:
            sigmas[c] = sum([sigmas[k] for k in relatives[c]["p"]])
        checked = checked.union(children)
        parents = children
        layers.append(copy.copy(children))
        children = set()
    flow = [1.0] * numNodes
    children = set()
    for i in xrange(numNodes):
        if not relatives[i]['c']:
            children.add(i)
    parents = set()
    checked = children
    while layers:
        layer = list(layers.pop())
        while layer:
            c = layer.pop()
            ancestors = relatives[c]['p']
            for k in ancestors:
                newflow = flow[c] * sigmas[k] / sigmas[c]
                if betweenAppr[SortedPair(c, k)] <= 5 * numNodes:
                    betweenAppr[SortedPair(c, k)] += newflow
                    betweenK[SortedPair(c, k)] += 1
                flow[k] += newflow

for e in edgeList:
    betweenAppr[e] = betweenAppr[e] * numNodes / betweenK[e]

# Plot
a = sorted(between.values(), reverse = True)
b = sorted(betweenAppr.values(), reverse = True)
p1, = plt.plot(range(len(a)), a, color = '#468499')
p2, = plt.plot(range(len(b)), b, color = '#fa8072')
plt.yscale('log')
plt.legend((p1, p2), ('Exact', 'Approximate'))
plt.title("Two Algorithms for Betweenness Centrality of Edges")
plt.ylabel('Betweenness')
plt.xlabel('Rank')
plt.savefig('between.pdf')
plt.close()
