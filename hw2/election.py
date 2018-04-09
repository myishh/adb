import snap
import matplotlib.pyplot as plt

# 2.1

def InitVote():
    vote = {}
    for k in xrange(10000):
        if k % 10 >= 8:
            vote[k] = 'U'
        elif k% 10 <= 3:
            vote[k] = 'A'
        else:
            vote[k] = 'B'
    return vote

def flip(k):
    if k == 'A': return 'B'
    else: return 'A'

def decision(vote, G, undecided):
    alternate = 'A'
    for _ in xrange(10):
        for p in undecided:
            NI = G.GetNI(p)
            d = NI.GetDeg()
            friends = {'A': 0, 'B': 0, 'U': 0}
            for nth in xrange(d):
                friends[vote[NI.GetNbrNId(nth)]] += 1
            if friends['A'] > friends['B']:
                vote[p] = 'A'
            elif friends['A'] < friends['B']:
                vote[p] = 'B'
            else:
                vote[p] = alternate
                alternate = flip(alternate)

    total = {'A':0, 'B':0}
    for k in xrange(10000):
        total[vote[k]] += 1
    return total

# 2.1
G1 = snap.PUNGraph.New()
with open("graph1.txt") as f:
    for line in f:
        a, b = line.split()
        if not G1.IsNode(int(a)): G1.AddNode(int(a))
        if not G1.IsNode(int(b)): G1.AddNode(int(b))
        G1.AddEdge(int(a), int(b))

undecided = [k for k in xrange(10000) if k % 10 >= 8]
vote = InitVote()
result = decision(vote, G1, undecided)
print result

G2 = snap.PUNGraph.New()
with open("graph2.txt") as f:
    for line in f:
        a, b = line.split()
        if not G2.IsNode(int(a)): G2.AddNode(int(a))
        if not G2.IsNode(int(b)): G2.AddNode(int(b))
        G2.AddEdge(int(a), int(b))

undecided = [k for k in xrange(10000) if k % 10 >= 8]
vote = InitVote()
result = decision(vote, G2, undecided)
print result

# 2.2
winby1 = []
for m in xrange(1, 10):
    vote = InitVote()
    influence = range(3000, 3000 + 10 * m)
    for index in influence:
        vote[index] = 'A'
    undecided = [k for k in xrange(10000) if k % 10 >= 8 and k not in influence]
    result = decision(vote, G1, undecided)
    winby1.append(result['A'] - result['B'])
print winby1

winby2 = []
for m in xrange(1, 10):
    vote = InitVote()
    influence = range(3000, 3000 + 10 * m)
    for index in influence:
        vote[index] = 'A'
    undecided = [k for k in xrange(10000) if k % 10 >= 8 and k not in influence]
    result = decision(vote, G2, undecided)
    winby2.append(result['A'] - result['B'])
print winby2

money = [i * 1000 for i in xrange(1, 10)]
p1, = plt.plot(money, winby1, color = "#45e890")
p2, = plt.plot(money, winby2, color = "#ff7400")
plt.grid()
plt.legend((p1, p2), ("Graph1", "Graph2"))
plt.title("The number of votes candidate A wins by VS Money spent on advertisement")
plt.xlabel('Money')
plt.ylabel("Win By")
plt.savefig("winby.pdf")
plt.close()

# 2.3
degrees1 = {index:G1.GetNI(index).GetDeg() for index in xrange(10000)}
ds = sorted(degrees1.items(), key = lambda x: x[1], reverse = True)
winby1 = []
for m in xrange(1, 10):
    vote = InitVote()
    rollers = [ds[k][0] for k in xrange(m)]
    for index in rollers:
        vote[index] = 'A'
    undecided = [k for k in xrange(10000) if k % 10 >= 8 and k not in rollers]
    result = decision(vote, G1, undecided)
    winby1.append(result['A'] - result['B'])
print winby1

degrees2 = {index:G2.GetNI(index).GetDeg() for index in xrange(10000)}
ds = sorted(degrees2.items(), key = lambda x: x[1], reverse = True)
winby2 = []
for m in xrange(1, 10):
    vote = InitVote()
    rollers = [ds[k][0] for k in xrange(m)]
    for index in rollers:
        vote[index] = 'A'
    undecided = [k for k in xrange(10000) if k % 10 >= 8 and k not in rollers]
    result = decision(vote, G2, undecided)
    winby2.append(result['A'] - result['B'])
print winby2

money = [i * 1000 for i in xrange(1, 10)]
p1, = plt.plot(money, winby1, color = "#45e890")
p2, = plt.plot(money, winby2, color = "#ff7400")
plt.grid()
plt.legend((p1, p2), ("Graph1", "Graph2"))
plt.title("The number of votes candidate A wins by VS Money spent on high rollers")
plt.xlabel('Money')
plt.ylabel("Win By")
plt.savefig("roller.pdf")
plt.close()

# 2.4
degrees1 = list()
counts1 = list()
DegToCntV = snap.TIntPrV()
snap.GetDegCnt(G1, DegToCntV)
for item in DegToCntV:
    degrees1.append(item.GetVal1())
    counts1.append(item.GetVal2())
# Normalize the counts
counts1 = [value / (1.0 * 10000) for value in counts1]

degrees2 = list()
counts2 = list()
DegToCntV = snap.TIntPrV()
snap.GetDegCnt(G2, DegToCntV)
for item in DegToCntV:
    degrees2.append(item.GetVal1())
    counts2.append(item.GetVal2())
# Normalize the counts
counts2 = [value / (1.0 * 10000) for value in counts2]

p1, = plt.plot(degrees1, counts1, color = "#45e890")
p2, = plt.plot(degrees2, counts2, color = "#ff7400")
plt.grid()
plt.legend((p1, p2), ("Graph1", "Graph2"))
plt.xscale('log')
plt.yscale('log')
plt.title("The Degree Distribution for 2 Graphs")
plt.savefig('degree.pdf')
plt.close()
