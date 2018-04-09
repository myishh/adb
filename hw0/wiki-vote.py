import snap

G = snap.LoadEdgeList(snap.PNGraph, "wiki-Vote.txt", 0, 1)

print "The number of nodes:", G.GetNodes()
print "The number of nodes with self-edges:" , snap.CntSelfEdges(G)
print "The number of directed edges:", snap.CntUniqDirEdges(G)
print "The number of undirected edges:", snap.CntUniqUndirEdges(G)
print "The number of reciprocated edges:", snap.CntUniqBiDirEdges(G)
print "The number of nodes with zero out-degree:", snap.CntOutDegNodes(G, 0)
print "The number of nodes with zero in-degree:", snap.CntInDegNodes(G, 0)
print "The number of nodes with more than 10 outgoing edges:", len([n for n in G.Nodes() if n.GetOutDeg() > 10])
print "The number of nodes with fewer than 10 incoming edges:", len([n for n in G.Nodes() if n.GetInDeg() < 10])
