import matplotlib.pyplot as plt

thresholds = []
with open('thresholds.txt') as f:
    for line in f:
        thresholds.append(int(line.split()[0]))

cumulative = [sum(thresholds[0:k + 1]) for k in xrange(1, len(thresholds))]
indice = [i for i in xrange(1, len(thresholds))]

for i in xrange(1, len(thresholds)):
    if sum(thresholds[0:i]) < i:
        print sum(thresholds[0:i])
        break

plt.bar(indice, cumulative, color = '#fa6e59', linewidth = 0)
plt.plot([0, 100], [1, 101], color = '#5294b1')
plt.title('Cumulative histogram of rioting thresholds')
plt.xlabel('Threshold')
plt.ylabel('Cumulative Number of People')
plt.xlim(xmax = len(thresholds))
plt.grid()
plt.savefig('histogram.pdf')
plt.close()
