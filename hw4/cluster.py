import numpy as np
import scipy.sparse as sparse
import snap
import numpy.linalg as la

# The function for calculating purity
def purity(labels, S):
    n = len(labels)
    a = 0
    b = 0
    for s in S:
        if labels[s] == 0: a += 1
        if labels[s] == 1: b += 1
    majority1 = max(a, b)
    Sbar = set(range(n)).difference(S)
    a = 0
    b = 0
    for s in Sbar:
        if labels[s] == 0: a += 1
        if labels[s] == 1: b += 1
    majority2 = max(a, b)
    return 1.0 * (majority1 + majority2) / n

# Get the labels
labels = []
with open("polblogs-labels.txt") as f:
    for line in f:
        labels.append(int(line.split()[0]))

# Construct the graph
G = snap.LoadEdgeList(snap.PUNGraph, "polblogs.txt", 0, 1)
numNodes = G.GetNodes()
numEdges = G.GetEdges()

degreeList = np.zeros(numNodes)
for node in G.Nodes():
    degreeList[node.GetId()] = node.GetDeg()

# Create adjacency matrix
row = []
col = []
data = []
for edge in G.Edges():
    n1 = edge.GetSrcNId()
    n2 = edge.GetDstNId()
    row += [n1, n2]
    col += [n2, n1]
    data += [1, 1]
adj = sparse.coo_matrix((data, (row, col)), shape=(numNodes, numNodes))

# Algorithm 1
laplacian = sparse.csgraph.laplacian(adj, normed = True)
egValues, egVectors = la.eigh(laplacian.toarray())
secondSmallest = sorted({i:egValues[i] for i in xrange(numNodes)}.items(), reverse = False)[1][0]
targetVec = egVectors[:,secondSmallest]
S1 = set()
for i in xrange(numNodes):
    if targetVec[i] > 0:
        S1.add(i)

print len(S1), numNodes - len(S1), purity(labels, S1)

# Algorithm 2
B = adj - (0.5 / numEdges) * np.dot(np.asmatrix(degreeList).T, np.asmatrix(degreeList))
egValues, egVectors = la.eigh(B)
largest = sorted({i:egValues[i] for i in xrange(numNodes)}.items(), reverse = True)[0][0]
targetVec = egVectors[:, largest]
S2 = set()
for i in xrange(numNodes):
    if targetVec[i] > 0:
        S2.add(i)

print len(S2), numNodes - len(S2), purity(labels, S2)
