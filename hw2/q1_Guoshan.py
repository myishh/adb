'''
This script is for hw2 question1
'''

from snap import *
import random
import numpy as np
import matplotlib.pyplot as plt

powerGrid=LoadEdgeList(PUNGraph,'USpowergrid_n4941.txt',0,1)


#/--------------------q1.1--------------------/
random.seed(0)
l_o_degree={}
for n in powerGrid.Nodes():
	l_o_degree[n.GetId()]=n.GetDeg()
stubs=[]
for n in l_o_degree:
	stubs+=([n]*l_o_degree[n])

l_o_cl_coef=[]
c=0
while(c<100):
	temp=stubs
	random.shuffle(temp)
	G=PUNGraph.New()
	for n in powerGrid.Nodes():
		G.AddNode(n.GetId())
	for i in xrange(len(temp)/2):
		G.AddEdge(temp[2*i],temp[2*i+1])
	if(CntUniqUndirEdges(G)==G.GetEdges()):
		c+=1
		l_o_cl_coef.append(GetClustCf(G, -1))
print np.mean(l_o_cl_coef)


#/--------------------q1.2--------------------/
random.seed(1)
l_o_edges=[]
for e in powerGrid.Edges():
	l_o_edges.append((e.GetSrcNId(),e.GetDstNId()))
l_o_cl_coef=[]
c=0
while(c<10000):
	sample=random.sample(l_o_edges,2)
	e1=sample[0]
	e2=sample[1]
	if(random.random()<0.5):
		u=e1[0]
		v=e1[1]
	else:
		u=e1[1]
		v=e1[0]
	if(random.random()<0.5):
		p=e2[0]
		q=e2[1]
	else:
		p=e2[1]
		q=e2[0]
	powerGrid.DelEdge(e1[0],e1[1])
	powerGrid.DelEdge(e2[0],e2[1])
	powerGrid.AddEdge(u,p)
	powerGrid.AddEdge(v,q)
	if(CntUniqUndirEdges(powerGrid)==powerGrid.GetEdges()):
		l_o_edges.remove(e1)
		l_o_edges.remove(e2)
		l_o_edges.append((u,p))
		l_o_edges.append((v,q))
		c+=1
	else:
		powerGrid.AddEdge(e1[0],e1[1])
		powerGrid.AddEdge(e2[0],e2[1])
		powerGrid.DelEdge(u,p)
		powerGrid.DelEdge(v,q)
		print 'badbad'
	if(c%100==0):
		l_o_cl_coef.append(GetClustCf(powerGrid, -1))
		print c
print l_o_cl_coef
plt.figure(1)
plt.plot(l_o_cl_coef,'b-')
plt.xlabel('Iteration Number')
plt.ylabel('Average Clusering Coeffient')
plt.savefig('AvgClC.png')












