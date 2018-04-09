import snap
import random
import matplotlib.pyplot as plt

NodeNum = 5242
EdgeNum = 14484
# Generate the graphs
# Erdos-Renyi Random graph
Graphs = [None] * 3
Graphs[0] = snap.GenRndGnm(snap.PUNGraph, NodeNum, EdgeNum, False)

# Small-World Random Network
Graphs[1] = snap.PUNGraph.New()
for i in range(NodeNum):
    Graphs[1].AddNode(i)
for i in range(0, NodeNum - 1):
    Graphs[1].AddEdge(i, i + 1)
Graphs[1].AddEdge(NodeNum - 1, 0)
for i in range(0, NodeNum - 2):
    Graphs[1].AddEdge(i, i + 2)
Graphs[1].AddEdge(NodeNum - 2, 0)
Graphs[1].AddEdge(NodeNum - 1, 1)

newones = 0
while newones < EdgeNum - 2 * NodeNum:
    i = random.randint(0, NodeNum - 1)
    j = random.randint(0, NodeNum - 1)
    if i != j and not Graphs[1].IsEdge(i, j) and not Graphs[1].IsEdge(j, i):
        Graphs[1].AddEdge(i, j)
        newones += 1

Graphs[2] = snap.LoadEdgeList(snap.PUNGraph, "ca-GrQc.txt", 0, 1)

# Counts the degrees of every node in the three graphs
degrees = [None] * 3
counts = [None] * 3
for g in range(3):
    degrees[g] = list()
    counts[g] = list()
    DegToCntV = snap.TIntPrV()
    snap.GetDegCnt(Graphs[g], DegToCntV)
    for item in DegToCntV:
        degrees[g].append(item.GetVal1())
        counts[g].append(item.GetVal2())
    # Normalize the counts
    counts[g] = [value / (1.0 * NodeNum) for value in counts[g]]

# Plot the degree distributions in log-scale
plots = [None] * 3
colors = ['#134c61', '#d97538', '#627f68']
for i in range(3):
    plots[i] ,= plt.plot(degrees[i], counts[i], color = colors[i])
plt.legend((plots[0], plots[1], plots[2]), ("Erdos-Renyi", "Small World", "Real World"))
plt.xscale('log')
plt.yscale('log')
plt.title("The Degree Distribution for Different Graphs")
plt.savefig('degree-distribution.eps')
plt.close()
# Report the average degree
for i in range(3):
    print sum([degrees[i][p] * counts[i][p] for p in range(len(counts[i]))])

# Calculate the excess degrees for three graphs
excesses = [None] * 3
for i in range(3):
    excesses[i] = {}
    for edge in Graphs[i].Edges():
        N1 = edge.GetSrcNId()
        d1 = Graphs[i].GetNI(N1).GetDeg()
        if (d1 - 1) not in excesses[i].keys():
            excesses[i][d1 - 1] = 1
        else:
            excesses[i][d1 - 1] += 1
        N2 = edge.GetDstNId()
        d2 = Graphs[i].GetNI(N1).GetDeg()
        if i == 0 and d2 == 17:
            print "Weird!"
        if (d2 - 1) not in excesses[i].keys():
            excesses[i][d2 - 1] = 1
        else:
            excesses[i][d2 - 1] += 1
    # Normalize the distribution values
    excesses[i] = {key: excesses[i][key] / (2.0 * EdgeNum) for key in excesses[i].keys()}

# Plot the excess distributions for three graphs
plots = [None] * 3
colors = ['#134c61', '#d97538', '#627f68']
for i in range(3):
    plots[i] ,= plt.plot(excesses[i].keys(), excesses[i].values(), color = colors[i])
plt.legend((plots[0], plots[1], plots[2]), ("Erdos-Renyi", "Small World", "Real World"))
plt.xscale('log')
plt.yscale('log')
plt.title("The Excess Degree Distribution for Different Graphs")
plt.savefig('excess-degree-distribution.eps')
plt.close()

# Report the average excess-degree
for i in range(3):
    print sum([excesses[i].keys()[p] * excesses[i].values()[p] for p in range(len(excesses[i].keys()))])

# Calculate the clustering coefficient
ccsums = [0] * 3
for g in range(3):
    graph = Graphs[g]
    for node in graph.Nodes():
        d = node.GetDeg()
        neighbors = []
        ee = 0
        if d >= 2:
            for n in range(d):
                new = node.GetNbrNId(n)
                for x in neighbors:
                    ee += graph.GetNI(x).IsNbrNId(new)
                neighbors.append(new)
            ccsums[g] += ee * 2.0 / (d * (d - 1))
    print ccsums[g] / NodeNum
    print snap.GetClustCf(Graphs[g], -1)
