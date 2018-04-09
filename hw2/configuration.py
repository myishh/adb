import snap
import random
import copy
import numpy as np
import matplotlib.pyplot as plt

# Function of returning a random edge iterator of an undirected graph
def randomEdge(Graph):
    num = Graph.GetEdges()
    i = random.randint(0, num - 1)
    EI = Graph.BegEI()
    k = 0
    while k < i:
        EI.Next()
        k += 1
    return EI

# The original graph
original = snap.LoadEdgeList(snap.PUNGraph, "USpowergrid_n4941.txt", 0, 1)
degreeList = snap.TIntV()
snap.GetDegSeqV(original, degreeList)

# The vector contain node i for k_i times, where k_i is the degree of node i
v = []
for i in xrange(degreeList.Len()):
    D = degreeList[i]
    v = v + [i for _ in xrange(D)]

# Generate 100 sample graphs
NodeNum = 100
Graphs = []
while len(Graphs) < 100:
    p = copy.copy(v)
    random.shuffle(p)
    sample = snap.GenRndGnm(snap.PUNGraph, NodeNum, 0, False)
    while len(p) != 0:
        id1 = p[-1]
        id2 = p[-2]
        if id1 != id2 and not sample.IsEdge(id1, id2):
            sample.AddEdge(id1, id2)
            p.pop()
            p.pop()
        else:
            random.shuffle(p)
    Graphs.append(sample)

# Compute the average clustering coefficient
clstCs = [snap.GetClustCf(g, -1) for g in Graphs]
print ("Average Clustering Coefficient for 100 Samples from Stub Matching Algorithm:", sum(clstCs) / len(clstCs))

# Rewiring
rG = snap.LoadEdgeList(snap.PUNGraph, "USpowergrid_n4941.txt", 0, 1)
iteration = 10000
rewiringCC = []
numEdge = rG.GetEdges()
for k in xrange(iteration):
    E1 = rG.BegEI()
    E2 = rG.BegEI()
    while True:
        E1 = randomEdge(rG)
        E2 = randomEdge(rG)
        IDS1 = E1.GetId()
        IDS2 = E2.GetId()

        # Check the validity of the selected two edges
        if IDS1[0] in IDS2 or IDS1[1] in IDS2:
            continue
        if rG.IsEdge(IDS1[0], IDS2[0]) or rG.IsEdge(IDS1[0], IDS2[1]) or rG.IsEdge(IDS1[1], IDS2[0]) or rG.IsEdge(IDS1[1], IDS2[1]):
            continue
        # Remove the selected edges and rewire them
        rG.DelEdge(IDS1[0], IDS1[1])
        rG.DelEdge(IDS2[0], IDS2[1])
        IDS1 = list(IDS1)
        IDS2 = list(IDS2)
        random.shuffle(IDS1)
        random.shuffle(IDS2)
        rG.AddEdge(IDS1[0], IDS2[0])
        rG.AddEdge(IDS1[1], IDS2[1])
        break

    if k % 100 == 0:
        rewiringCC.append(snap.GetClustCf(rG, -1))

plt.plot(np.arange(0, 10000, 100), rewiringCC, color = "#208ef1")
plt.title("Clustering Coefficient VS Iteration Number of Rewiring Algorithm")
plt.xlabel("Number of Iteration")
plt.ylabel("Clustering Coefficient")
plt.savefig("rewiring.pdf")
plt.close()
