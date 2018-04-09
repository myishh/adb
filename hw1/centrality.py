import snap
import pandas as pd
# Read in the data files
actorKey = pd.read_csv("imdb_actors_key.tsv", sep = '\t')
nodeMapping = snap.TStrIntSH()
actorNet = snap.LoadEdgeListStr(snap.PUNGraph, "imdb_actor_edges.tsv", 0, 1, nodeMapping)
LWCC = snap.GetMxWcc(actorNet)

# Find 20 actors with the largest degrees
degreeList = snap.TIntV()
snap.GetDegSeqV(LWCC, degreeList)
degreeDict= {i : degreeList[i] for i in xrange(degreeList.Len())}
sortedDegDict = sorted(degreeDict.items(), key = lambda x: x[1], reverse = True)
top20Degree = sortedDegDict[:20]

for item in top20Degree:
    print "Name:", actorKey[actorKey["ID"] == int(nodeMapping.GetKey(item[0]))]["name"].values[0], "Degree:", item[1]
    print "Main Genre:", actorKey[actorKey["ID"] == int(nodeMapping.GetKey(item[0]))]["main_genre"].values[0]
    print "Number:", actorKey[actorKey["ID"] == int(nodeMapping.GetKey(item[0]))]["movies_95_04"].values[0]

# Find 20 actors with the largest betweenness
nodesBetweenness = snap.TIntFltH()
edgesBetweenness = snap.TIntPrFltH()
snap.GetBetweennessCentr(LWCC, nodesBetweenness, edgesBetweenness, 1.0, False)
nodesBetweenness.SortByDat(False)
iterator = nodesBetweenness.BegI()
count = 0
while count < 20:
    print "Name:", actorKey[actorKey["ID"] == int(nodeMapping.GetKey(iterator.GetKey()))]["name"].values[0], "Betweenness:", iterator.GetDat()
    print "Main Genre:", actorKey[actorKey["ID"] == int(nodeMapping.GetKey(iterator.GetKey()))]["main_genre"].values[0]
    print "Number:", actorKey[actorKey["ID"] == int(nodeMapping.GetKey(iterator.GetKey()))]["movies_95_04"].values[0]
    count += 1
    iterator.Next()

closenessDict = {}
for NI in actorNet.Nodes():
    closenessDict[NI.GetId()] = snap.GetClosenessCentr(actorNet, NI.GetId())
sortedClsDict = sorted(closenessDict.items(), key = lambda x: x[1], reverse = True)
top20Cls = sortedClsDict[:20]
for item in top20Cls:
    print "Name:", actorKey[actorKey["ID"] == int(nodeMapping.GetKey(item[0]))]["name"].values[0], "Closeness:", item[1]
    print "Main Genre:", actorKey[actorKey["ID"] == int(nodeMapping.GetKey(item[0]))]["main_genre"].values[0]
    print "Number:", actorKey[actorKey["ID"] == int(nodeMapping.GetKey(item[0]))]["movies_95_04"].values[0]
