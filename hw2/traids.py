import snap
import random
# Signed Triads in Epinions
signedNet = snap.TNEANet.New()
signedNet.AddIntAttrE("sign")

# Read the file in and set attribute to every edge
with open("epinions-signed.txt") as f:
    for i, line in enumerate(f):
        if i >= 2:
            a,b,c = line.split()
            if a != b:
                if not signedNet.IsNode(int(a)):signedNet.AddNode(int(a))
                if not signedNet.IsNode(int(b)):signedNet.AddNode(int(b))
                EId = signedNet.AddEdge(int(a), int(b))
                signedNet.AddIntAttrDatE(EId, int(c), "sign")

# Count the number of different types of triads
counts = {-3:0, 3:0, -1:0, 1:0}
for node in signedNet.Nodes():
    A = node.GetId()
    degree = node.GetDeg()
    for i in xrange(degree):
        B = node.GetNbrNId(i)
        for j in xrange(i + 1, degree):
            C = node.GetNbrNId(j)
            if signedNet.GetNI(B).IsNbrNId(C) and B > A and C > A:
                EIs = []
                for p in [A, B, C]:
                    for q in [A, B, C]:
                        if signedNet.IsEdge(p, q):
                            EIs.append(signedNet.GetEI(p, q))
                counts[sum([signedNet.GetIntAttrDatE(EIs[i], "sign") for i in xrange(3)])] += 1

print counts
print {i :1.0 * counts[i] / sum(counts.values()) for i in counts.keys()}

# 2.4 Simulation
def IsBalancedTriangle(a, b, c, signs):
    judge = signs[(a, b)] + signs[(b, c)] + signs[(a, c)]
    if judge == -3 or judge == 1:
        return False
    else:
        return True

def IsBalancedGraph(NodeNum, signs):
    for i in xrange(NodeNum):
        for j in xrange(i + 1, NodeNum):
            for k in xrange(j + 1, NodeNum):
                judge = signs[(i, j)] + signs[(i, k)] + signs[(j, k)]
                if judge == -3 or judge == 1:
                    return False
    return True

def RandomTriad(NodeNum):
    a, b, c = 0, 0, 0
    while a == b or b == c or a == c:
        a = random.randint(0, NodeNum - 1)
        b = random.randint(0, NodeNum - 1)
        c = random.randint(0, NodeNum - 1)
    return sorted([a, b, c])

def RandomPair(a, b, c):
    k = random.choice([1, 2, 3])
    if k == 1:
        return (a, b)
    elif k == 2:
        return (a, c)
    else:
        return (b, c)


Balanced = 0
edges = []
NodeNum = 10
for i in xrange(NodeNum):
    for j in xrange(i + 1, NodeNum):
        edges.append((i, j))
for _ in xrange(100):
    signs = {pair : random.choice([-1, 1]) for pair in edges}
    for _ in xrange(10000000):
        a, b, c = RandomTriad(NodeNum)
        if not IsBalancedTriangle(a, b, c, signs):
            flip = RandomPair(a, b, c)
            signs[flip] = -signs[flip]
        if IsBalancedGraph(NodeNum, signs):
            Balanced += 1
            break
print Balanced
