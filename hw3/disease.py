import snap
import random
import scipy.stats as stats

def infect(graph, beta, delta):
    nodeIDlist = list()
    for node in graph.Nodes():
        nodeIDlist.append(node.GetId())
    states = {'S':set(nodeIDlist), 'I':set([]), 'R':set([])}
    first = random.sample(set(nodeIDlist), 1)[0]
    states['I'].add(first)
    states['S'].remove(first)
    while len(states['I']) != 0:
        for node in graph.Nodes():
            nodeID = node.GetId()
            if nodeID in states['S']:
                degree = node.GetDeg()
                for nbr in xrange(degree):
                    neighborID = node.GetNbrNId(nbr)
                    if neighborID in states['I']:
                        infect = random.random()
                        if infect < beta:
                            states['I'].add(nodeID)
                            states['S'].remove(nodeID)
                            break
            elif nodeID in states['I']:
                recover = random.random()
                if recover < delta:
                    states['R'].add(nodeID)
                    states['I'].remove(nodeID)
    return {'R': len(states['R']), 'S': len(states['S'])}

def infecthigh(graph, beta, delta):
    nodeIDlist = list()
    degrees = {}
    for node in graph.Nodes():
        nodeIDlist.append(node.GetId())
        degrees[node.GetId()] = node.GetDeg()
    states = {'S':set(nodeIDlist), 'I':set([]), 'R':set([])}
    sortedDeg = sorted(degrees.items(), key = lambda x: x[1], reverse = True)
    first = sortedDeg[0][0]
    states['I'].add(first)
    states['S'].remove(first)
    while len(states['I']) != 0:
        for node in graph.Nodes():
            nodeID = node.GetId()
            if nodeID in states['S']:
                degree = node.GetDeg()
                for nbr in xrange(degree):
                    neighborID = node.GetNbrNId(nbr)
                    if neighborID in states['I']:
                        infect = random.random()
                        if infect < beta:
                            states['I'].add(nodeID)
                            states['S'].remove(nodeID)
                            break
            elif nodeID in states['I']:
                recover = random.random()
                if recover < delta:
                    states['R'].add(nodeID)
                    states['I'].remove(nodeID)
    return {'R': len(states['R']), 'S': len(states['S'])}

def infect10(graph, beta, delta):
    nodeIDlist = list()
    for node in graph.Nodes():
        nodeIDlist.append(node.GetId())
    states = {'S':set(nodeIDlist), 'I':set([]), 'R':set([])}
    for _ in xrange(10):
        some = random.sample(states['S'], 1)[0]
        states['I'].add(some)
        states['S'].remove(some)
    while len(states['I']) != 0:
        for node in graph.Nodes():
            nodeID = node.GetId()
            if nodeID in states['S']:
                degree = node.GetDeg()
                for nbr in xrange(degree):
                    neighborID = node.GetNbrNId(nbr)
                    if neighborID in states['I']:
                        infect = random.random()
                        if infect < beta:
                            states['I'].add(nodeID)
                            states['S'].remove(nodeID)
                            break
            elif nodeID in states['I']:
                recover = random.random()
                if recover < delta:
                    states['R'].add(nodeID)
                    states['I'].remove(nodeID)
    return {'R': len(states['R']), 'S': len(states['S'])}

def infecthigh10(graph, beta, delta):
    nodeIDlist = list()
    degrees = {}
    for node in graph.Nodes():
        nodeIDlist.append(node.GetId())
        degrees[node.GetId()] = node.GetDeg()
    states = {'S':set(nodeIDlist), 'I':set([]), 'R':set([])}
    sortedDeg = sorted(degrees.items(), key = lambda x: x[1], reverse = True)
    for t in range(10):
        some = sortedDeg[t][0]
        states['S'].remove(some)
        states['I'].add(some)
    while len(states['I']) != 0:
        for node in graph.Nodes():
            nodeID = node.GetId()
            if nodeID in states['S']:
                degree = node.GetDeg()
                for nbr in xrange(degree):
                    neighborID = node.GetNbrNId(nbr)
                    if neighborID in states['I']:
                        infect = random.random()
                        if infect < beta:
                            states['I'].add(nodeID)
                            states['S'].remove(nodeID)
                            break
            elif nodeID in states['I']:
                recover = random.random()
                if recover < delta:
                    states['R'].add(nodeID)
                    states['I'].remove(nodeID)
    return {'R': len(states['R']), 'S': len(states['S'])}

beta = 0.05
delta = 0.5
Graphs = {}
Graphs['actor'] = snap.LoadEdgeList(snap.PUNGraph, "imdb_actor_edges.tsv", 0, 1)
Graphs['erdos'] = snap.LoadEdgeList(snap.PUNGraph, "SIR_erdos_renyi.txt", 0, 1)
Graphs['pref'] = snap.LoadEdgeList(snap.PUNGraph, "SIR_preferential_attachment.txt", 0, 1)
keys = ['actor', 'erdos', 'pref']

#
# print 'Problem 1:'
# results = {key :[] for key in keys}
# for _ in xrange(100):
#     for key in Graphs.keys():
#         results[key].append(infect(Graphs[key], beta, delta))
# chi_data = {key:0 for key in keys}
# for key in keys:
#     result = results[key]
#     chi_data[key] = sum([1 for item in result if item['R'] >= item['S']])
# print chi_data
# print stats.chi2_contingency([[chi_data['actor'], 100-chi_data['actor']],[chi_data['erdos'], 100-chi_data['erdos']]])
# print stats.chi2_contingency([[chi_data['actor'], 100-chi_data['actor']],[chi_data['pref'], 100-chi_data['pref']]])
# print stats.chi2_contingency([[chi_data['erdos'], 100-chi_data['erdos']],[chi_data['pref'], 100-chi_data['pref']]])
# epidemic = {key:[] for key in keys}
# for key in keys:
#     result = results[key]
#     for item in result:
#         if item['R'] >= item['S']:
#             epidemic[key].append(1.0 * item['R'] / (item['R'] + item['S']))
# print stats.mannwhitneyu(epidemic['actor'], epidemic['erdos'])
# print stats.mannwhitneyu(epidemic['actor'], epidemic['pref'])
# print stats.mannwhitneyu(epidemic['erdos'], epidemic['pref'])
# print {key : 1.0 * sum(epidemic[key]) / len(epidemic[key]) for key in keys}
# whole = {key:[] for key in keys}
# for key in keys:
#     result = results[key]
#     for item in result:
#         whole[key].append(1.0 * item['R'] / (item['R'] + item['S']))
# print stats.mannwhitneyu(whole['actor'], whole['erdos'])
# print stats.mannwhitneyu(whole['actor'], whole['pref'])
# print stats.mannwhitneyu(whole['erdos'], whole['pref'])
# print {key : 1.0 * sum(whole[key]) / len(whole[key]) for key in keys}
#
# print 'Problem 2:'
# results2 = {key :[] for key in Graphs.keys()}
# for _ in xrange(100):
#     for key in Graphs.keys():
#         results2[key].append(infecthigh(Graphs[key], beta, delta))
#
# chi_data2 = {key:0 for key in keys}
# for key in keys:
#     result = results2[key]
#     chi_data2[key] = sum([1 for item in result if item['R'] >= item['S']])
# print chi_data2
# epidemic2 = {key:[] for key in keys}
# for key in keys:
#     result = results2[key]
#     for item in result:
#         if item['R'] >= item['S']:
#             epidemic2[key].append(1.0 * item['R'] / (item['R'] + item['S']))
# print stats.mannwhitneyu(epidemic2['actor'], epidemic2['erdos'])
# print stats.mannwhitneyu(epidemic2['actor'], epidemic2['pref'])
# print stats.mannwhitneyu(epidemic2['erdos'], epidemic2['pref'])
# print {key : 1.0 * sum(epidemic2[key]) / len(epidemic2[key]) for key in keys}
# whole2 = {key:[] for key in keys}
# for key in keys:
#     result = results2[key]
#     for item in result:
#         whole2[key].append(1.0 * item['R'] / (item['R'] + item['S']))
# print stats.mannwhitneyu(whole2['actor'], whole2['erdos'])
# print stats.mannwhitneyu(whole2['actor'], whole2['pref'])
# print stats.mannwhitneyu(whole2['erdos'], whole2['pref'])
# print {key : 1.0 * sum(whole2[key]) / len(whole2[key]) for key in keys}

print 'Problem 3:'
results3 = {key :[] for key in Graphs.keys()}
for _ in xrange(100):
    for key in Graphs.keys():
        results3[key].append(infect10(Graphs[key], beta, delta))
chi_data3 = {key:0 for key in keys}
for key in keys:
    result = results3[key]
    chi_data3[key] = sum([1 for item in result if item['R'] >= item['S']])
print chi_data3
epidemic3 = {key:[] for key in keys}
for key in keys:
    result = results3[key]
    for item in result:
        if item['R'] >= item['S']:
            epidemic3[key].append(1.0 * item['R'] / (item['R'] + item['S']))
print stats.mannwhitneyu(epidemic3['actor'], epidemic3['erdos'])
print stats.mannwhitneyu(epidemic3['actor'], epidemic3['pref'])
print stats.mannwhitneyu(epidemic3['erdos'], epidemic3['pref'])
print {key : 1.0 * sum(epidemic3[key]) / len(epidemic3[key]) for key in keys}
whole3 = {key:[] for key in keys}
for key in keys:
    result = results3[key]
    for item in result:
        whole3[key].append(1.0 * item['R'] / (item['R'] + item['S']))
print stats.mannwhitneyu(whole3['actor'], whole3['erdos'])
print stats.mannwhitneyu(whole3['actor'], whole3['pref'])
print stats.mannwhitneyu(whole3['erdos'], whole3['pref'])
print {key : 1.0 * sum(whole3[key]) / len(whole3[key]) for key in keys}

print 'Problem 4:'
results4 = {key :[] for key in Graphs.keys()}
for _ in xrange(100):
    for key in Graphs.keys():
        results4[key].append(infecthigh10(Graphs[key], beta, delta))
chi_data4 = {key:0 for key in keys}
for key in keys:
    result = results4[key]
    chi_data4[key] = sum([1 for item in result if item['R'] >= item['S']])
print chi_data4
epidemic4 = {key:[] for key in keys}
for key in keys:
    result = results4[key]
    for item in result:
        if item['R'] >= item['S']:
            epidemic4[key].append(1.0 * item['R'] / (item['R'] + item['S']))
print stats.mannwhitneyu(epidemic4['actor'], epidemic4['erdos'])
print stats.mannwhitneyu(epidemic4['actor'], epidemic4['pref'])
print stats.mannwhitneyu(epidemic4['erdos'], epidemic4['pref'])
print {key : 1.0 * sum(epidemic4[key]) / len(epidemic4[key]) for key in keys}
whole4 = {key:[] for key in keys}
for key in keys:
    result = results4[key]
    for item in result:
        whole4[key].append(1.0 * item['R'] / (item['R'] + item['S']))
print stats.mannwhitneyu(whole4['actor'], whole4['erdos'])
print stats.mannwhitneyu(whole4['actor'], whole4['pref'])
print stats.mannwhitneyu(whole4['erdos'], whole4['pref'])
print {key : 1.0 * sum(whole4[key]) / len(whole4[key]) for key in keys}
