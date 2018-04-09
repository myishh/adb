import snap
import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt

# The function to calculate the distance between two Network of the virtual tree
def distance(NId1, NId2, b, H):
    # NId1 and NId2 are the IDs of two nodes
    # b is the number of each parent's children
    # H is the height of the tree
    dist = H
    for i in range(H):
        test = H - i
        if NId1 * b / (b ** test) == NId2 * b / (b ** test):
            dist -= 1
        else:
            break
    return dist

# The function for decentralized search
# Given a graph and two node IDs
# step is the number that the source already gone through
def search(Graph, ID1, ID2, step):
    if Graph.IsEdge(ID1, ID2):
        return step + 1
    else:
        neighbors = {}
        for i in xrange(5):
            other = Graph.GetNI(ID1).GetOutNId(i)
            neighbors[other] = distance(other, ID2, 2, 10)
        S = sorted(neighbors.items(), key = lambda x: x[1])
        if S[0][1] < distance(ID1, ID2, 2, 10):
            return search(Graph, S[0][0], ID2, step + 1)
        else:
            return 0

# The basic parameters of the problem
NodeNum = 1024
EdgeNum = 0
b = 2
H = 10
IdList = range(NodeNum)
Sampling = list(np.ones(NodeNum) / float(NodeNum))

# Construct the list of alphas and the dictionary of results
alphas = [i * 0.1 for i in range(1, 101)]
paths = []
rates = []

# For different alpha, construct new graphs and do the same calculation
for alpha in alphas:
    # Generate an empty graph with 1024 nodes and no edges
    Network = snap.GenRndGnm(snap.PNGraph, NodeNum, EdgeNum, True)
    for node in Network.Nodes():
        center = node.GetId()
        chosen = []
        probs = np.array([b ** (-alpha * distance(center, other, b, H)) for other in IdList])
        probs[center] = 0
        for i in range(5):
            for some in chosen:
                probs[chosen] = 0
            probs = probs / sum(probs)
            new = np.random.choice(IdList, 1, p = list(probs))[0]
            chosen.append(new)
            Network.AddEdge(center, new)

    # Do decentralized search in the constructed network
    successes = 0
    sumpath = 0
    for k in xrange(1000):
        samples = np.random.choice(IdList, 2, replace = False, p = Sampling)
        s = samples[0]
        t = samples[1]
        searching = search(Network, s, t, 0)
        if searching != False:
            successes += 1
            sumpath += searching
    rates.append(successes / 1000.0)
    paths.append(sumpath / float(successes))

plt.plot(alphas, rates)
plt.xlabel("The value of alpha")
plt.ylabel("Success Rate")
plt.title("Success Rates for Decentralized Search")
plt.savefig("rates.eps")
plt.close()

plt.plot(alphas, paths)
plt.xlabel("The value of alpha")
plt.ylabel("The Average Length of Path")
plt.ylim(ymin = 0)
plt.title("Average Path Length for Decentralized Search")
plt.savefig("length.eps")
plt.close()
