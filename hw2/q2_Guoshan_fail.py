################################################################################
# Starter code for Problem 2
# Author: poorvib@stanford.edu
# Last Updated: Oct 4, 2017
# Note: This starter code is only one possible implementation for this question.
# Please feel free to implement your own solution and/or modify this code in
# any way that you need.
################################################################################

import snap
import random
import numpy as np

# Problem 2.1 Functions
def loadSigns(filename):
    """
    :param - filename: undirected graph with associated edge sign

    return type: dictionary (key = node pair (a,b), value = sign)
    return: Return sign associated with node pairs. Both pairs, (a,b) and (b,a)
    are stored as keys. Self-edges are NOT included.
    """
    signs = {}
    with open(filename, 'r') as ipfile:
    	for line in ipfile:
            if line[0] != '#':
                line_arr = line.split()
                if line_arr[0] == line_arr[1]:
    				continue
                node1 = int(line_arr[0])
                node2 = int(line_arr[1])
                sign = int(line_arr[2])
                signs[(node1, node2)] = sign
                signs[(node2, node1)] = sign
    return signs

def getNeibNodes(G,signs,NI):
    """
    :param G:
    :param signs:
    :param NI:
    :return: a set of neibrhood nodes
    """

    x = [list(key) for key, value in signs.iteritems() if NI in key]
    [i.remove(NI) for i in x]
    x = [i[0] for i in x]
    neibor_nodes = set(x)

    return neibor_nodes

def computeTriadCounts(G, signs):
    """
    :param - G: graph
    :param - signs: Dictionary of signs (key = node pair (a,b), value = sign)

    return type: List, each position representing count of t0, t1, t2, and t3, respectively.
    return: Return the counts for t0, t1, t2, and t3 triad types. Count each triad
    only once and do not count self edges.
    """

    triad_count = [0, 0, 0, 0] # each position represents count of t0, t1, t2, t3, respectively

    ############################################################################
    visited_triads = [] # storing sets of visited triads node

    for key, value in signs.iteritems(): # iterate all the edges in the graph

        n1, n2 = key[0],key[1] # get the two nodes of an edge
        print 'iterating sign with node %i %i' %(n1,n2)

        if n1 == n2: #skip self connected edge
            continue

        n_common_nodes = snap.GetCmnNbrs(G, n1, n2) # see how many common neigbors the two nodes share

        print 'there are %i common nodes' %(n_common_nodes)

        if n_common_nodes > 0: # if there is more than 1 common shared neigbor, means there is a triad

            print 'finding common neigbors'

            neib_n1 = getNeibNodes(G,signs,n1)

            neib_n2 = getNeibNodes(G,signs,n2)

            common_neib = list(neib_n1.intersection(neib_n2)) # get common shared neibor nodes

            print 'the common nodes are', common_neib

            assert len(common_neib) == n_common_nodes # check if own written function gets the same result as GetCmnNbrs

            for node in common_neib:

                if n2 == node or n1 == node: # skip self connected edge
                    continue

                triad = set((n1,n2,node)) # form triad

                print 'form triad: ', triad

                if triad not in visited_triads:

                    print 'the formed triad not in visited triads'

                    # count signs and increment type
                    sum_signs = signs[(n1,n2)]+signs[(n2,node)]+signs[(n1,node)]

                    print 'sum signs is %i' %sum_signs
                    if sum_signs == -3:
                        triad_count[0] += 1
                    elif sum_signs == -1:
                        triad_count[1] += 1
                    elif sum_signs == 1:
                        triad_count[2] += 1
                    else:
                        triad_count[3] += 1

                    # append to visited triad
                    visited_triads.append(triad)
                    print 'append to visited triads'

    ############################################################################

    return triad_count

def displayStats(G, signs):
    '''
    :param - G: graph
    :param - signs: Dictionary of signs (key = node pair (a,b), value = sign)

    Computes and prints the fraction of positive edges and negative edges,
        and the probability of each type of triad.
    '''
    fracPos = 0
    fracNeg = 0
    probs = [0,0,0,0]

    ############################################################################
    # TODO: Your code here! (Note: you may not need both input parameters)
    pos_count = [1 for key, value in signs.iteritems() if value == 1 ]
    total_signs = len(signs)
    pos_signs = len(pos_count)
    fracPos = pos_signs/float(total_signs)
    fracNeg = 1 - fracPos

    type0_prob = fracNeg ** 3
    type3_prob = fracPos ** 3
    type1_prob = 3 * fracPos * fracNeg * fracNeg
    type2_prob = 3 * fracNeg * fracPos * fracPos

    probs = [type0_prob,type1_prob,type2_prob,type3_prob]

    ############################################################################

    print 'Fraction of Positive Edges: %0.4f' % (fracPos)
    print 'Fraction of Negative Edges: %0.4f' % (fracNeg)

    for i in range(4):
        print "Probability of Triad t%d: %0.4f" % (i, probs[i])

# Problem 2.4 Functions
def createCompleteNetwork(networkSize):
    """
    :param - networkSize: Desired number of nodes in network

    return type: Graph
    return: Returns complete network on networkSize
    """
    completeNetwork = None
    ############################################################################
    # TODO: Your code here!
    completeNetwork = snap.TUNGraph.New()

    # Add nodes
    for i in range(networkSize):
        completeNetwork.AddNode(i)

    # Add edges
    for i in range(networkSize-1):
        for j in range(i+1,networkSize):
            completeNetwork.AddEdge(i,j)
            j += 1
        i += 1

    ############################################################################
    return completeNetwork

def assignRandomSigns(G):
    """
    :param - G: Graph

    return type: dictionary (key = node pair (a,b), value = sign)
    return: For each edge, a sign (+, -) is chosen at random (p = 1/2).
    """
    signs = {}
    ############################################################################
    # TODO: Your code here!
    for EI in G.Edges():
        print "edge (%d, %d)" % (EI.GetSrcNId(), EI.GetDstNId())
        signs[(EI.GetSrcNId(), EI.GetDstNId())] = np.random.choice([1,-1])

    assert len(signs) == G.GetEdges()

    ############################################################################
    return signs

def runDynamicProcess(G, signs, num_iterations):
    """
    :param - G: Graph
    :param - signs: Dictionary of signs (key = node pair (a,b), value = sign)
    :param - num_iterations: number of iterations to run dynamic process

    Runs the dynamic process described in problem 2.3 for num_iterations iterations.
    """
    ############################################################################
     # TODO: Your code here!

    N = G.GetNodes()
    i = 1

    while i < num_iterations:

        if isBalancedNetwork(G, signs):
            print 'already balanced, skip the remaining update'
            break

        # pick a random triad 3 nodes
        nodes = np.random.choice(N,3,replace = False)
        nodes.sort()

        print 'selected 3 nodes are: ', nodes

        # check if it is balanced
        e1 = signs[(nodes[0],nodes[1])]
        e2 = signs[(nodes[0],nodes[2])]
        e3 = signs[(nodes[1],nodes[2])]

        sum = np.sum([e1,e2,e3])

        # if not balanced
        if sum == 1 or sum == -3:
            print 'not balanced'
            # random choose 2 nodes
            rdnodes = np.random.choice(nodes,2,replace = False)
            rdnodes.sort()
            print 'selected flip edge 2 nodes are: ', rdnodes
            # flip the sign
            signs[tuple(rdnodes)] *= -1

        i += 1


    ############################################################################

def isBalancedNetwork(G, signs):
    """
    :param - G: Graph
    :param - signs: Dictionary of signs (key = node pair (a,b), value = sign)

    return type: Boolean
    return: Returns whether G is balanced (True) or not (False).
    """
    isBalanced = False
    ############################################################################
    # TODO: Your code here!

    N = G.GetNodes()

    for i in range(N-2):
        for j in range(i+1, N-1):
            for k in range(j+1, N):
                # check if it is balanced
                e1 = signs[(i,j)]
                e2 = signs[(i,k)]
                e3 = signs[(j,k)]

                sum = np.sum([e1,e2,e3])

                # if not balanced
                if sum == 1 or sum == -3:
                    return isBalanced

    isBalanced = True

    ############################################################################
    return isBalanced

def computeNumBalancedNetworks(numSimulations):
    """
    :param - numSimulations: number of simulations to run

    return type: Integer
    return: Returns number of networks that end up balanced.
    """
    numBalancedNetworks = 0

    for iteration in range(0, numSimulations):
        # (I) Create complete network on 10 nodes
        simulationNetwork = createCompleteNetwork(10)

        # (II) For each edge, choose a sign (+,-) at random (p = 1/2)
        signs = assignRandomSigns(simulationNetwork)

        # (III) Run dynamic process
        num_iterations = 1000000
        runDynamicProcess(simulationNetwork, signs, num_iterations)

        # determine whether network is balanced
        if isBalancedNetwork(simulationNetwork, signs):
            numBalancedNetworks += 1

    return numBalancedNetworks

def main():
    filename = "epinions-signed.txt"

    # load Graph and Signs
    epinionsNetwork = snap.LoadEdgeList(snap.PUNGraph, filename, 0, 1)
    signs = loadSigns(filename)

    # Compute Triad Counts
    triad_count = computeTriadCounts(epinionsNetwork, signs)

    # Problem 2.1a
    print "Problem 2.1a"
    for i in range(4):
        print "Count of Triad t%d: %d" % (i, triad_count[i])

    total_triads = float(sum(triad_count)) if sum(triad_count) != 0 else 1
    for i in range(4):
        print "Fraction of Triad t%d: %0.4f" % (i, triad_count[i]/total_triads)

    # Problem 2.1b
    print "Problem 2.1b"
    displayStats(epinionsNetwork, signs)

    # Problem 2.4
    print "Problem 2.4"
    networkSize = 10
    numSimulations = 100
    numBalancedNetworks = computeNumBalancedNetworks(numSimulations)
    print "Fraction of Balanced Networks: %0.4f" % (float(numBalancedNetworks)/float(numSimulations))


if __name__ == '__main__':
	main()
