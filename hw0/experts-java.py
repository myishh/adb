import snap

G = snap.LoadEdgeList(snap.PNGraph, "stackoverflow-Java.txt", 0, 1)
Components = snap.TCnComV()
snap.GetWccs(G, Components)
print "NUmber of weakly connected components:", len(Components)

MxWcc = snap.GetMxWcc(G)
print "Number of nodes in the largest weakly connected component:", MxWcc.GetNodes()
print "Number of edges in the largest weakly connected component:", MxWcc.GetEdges()

PRankH = snap.TIntFltH()
snap.GetPageRank(G, PRankH)
PRankH.SortByDat(False)

i = 0
itr = PRankH.BegI()
print "The top 3 most central nodes in the network by PagePank scores:"
while i < 3:
    print "Node", itr.GetKey()
    itr.Next()
    i += 1

NIdHubH = snap.TIntFltH()
NIdAuthH = snap.TIntFltH()
snap.GetHits(G, NIdHubH, NIdAuthH)
NIdHubH.SortByDat(False)
i = 0
itr = NIdHubH.BegI()
print "The top 3 hubs in the network by HITS score:"
while i < 3:
    print "Node", itr.GetKey()
    itr.Next()
    i += 1

NIdAuthH.SortByDat(False)
i = 0
itr = NIdAuthH.BegI()
print "The top 3 authorities in the network by HITS score:"
while i < 3:
    print "Node", itr.GetKey()
    itr.Next()
    i += 1
