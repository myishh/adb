import random
import matplotlib.pyplot as plt
import numpy as np

# Problem 2.2
samples = {}
for _ in xrange(100000):
    u = random.random()
    sample = round(1/u)
    if sample not in samples.keys():
        samples[sample] = 1
    else:
        samples[sample] += 1

pairs = sorted(samples.items(), key = lambda x: x[0])
keys = []
freqs = []
x = [0.1 * i for i in xrange(10, 10000)]
y = [t ** (-2) for t in x]
for k, v in pairs:
    keys.append(k)
    freqs.append(v / 100000.0)
plot1, = plt.plot(keys, freqs, color = '#fa6e59')
plot2, = plt.plot(x, y, color = '#5294b1')
plt.title("Empiricla Distribution VS Theoretical Distribution")
plt.legend((plot1, plot2), ('Empirical Dist', 'Probability Dist'))
plt.xlabel("Sample")
plt.ylabel("Frequency")
plt.xscale('log')
plt.yscale('log')
plt.savefig('samples.pdf')
plt.close()

# Problem 2.3
x1 = np.log(np.array(keys))
y1 = np.log(np.array(freqs))
A = np.vstack([x1, np.ones(len(x1))]).T
slope, intercept = np.linalg.lstsq(A, y1)[0]
print slope, intercept
yfit1 = [t ** (slope) for t in x]

x2 = np.log(np.array([k for k in keys if k <= 100]))
y2 = np.log(np.array(freqs[0:len(x2)]))
A = np.vstack([x2, np.ones(len(x2))]).T
slope, intercept = np.linalg.lstsq(A, y2)[0]
print slope, intercept
yfit2 = [t ** (slope) for t in x]

plot1, = plt.plot(keys, freqs, color = '#fa6e59')
plot2, = plt.plot(x, y, color = '#5294b1')
plot3, = plt.plot(x, yfit1, color = '#9a3159')
plot4, = plt.plot(x, yfit2, color = '#bc8360')
plt.title("Empiricla Distribution VS Theoretical Distribution")
plt.legend((plot1, plot2, plot3, plot4), ('Empirical Dist', 'Probability Dist', 'Least-Square Using All Data', 'Least-square Ignoring Some Data '))
plt.xlabel("Sample")
plt.ylabel("Frequency")
plt.xscale('log')
plt.yscale('log')
plt.savefig('fit.pdf')
plt.close()

# Problem 2.4
x3 = np.log(np.array(keys))
y3 = np.log(np.array([sum(freqs[0:k+1]) for k in xrange(len(freqs))]))
A = np.vstack([x3, np.ones(len(x3))]).T
slope, intercept = np.linalg.lstsq(A, y3)[0]
print slope, intercept
yfit3 = [t ** (slope - 1) for t in x]

plot1, = plt.plot(keys, freqs, color = '#fa6e59')
plot2, = plt.plot(x, y, color = '#5294b1')
plot5, = plt.plot(x, yfit3, color = '#9a3159')
plt.title("Distributions and Estimation")
plt.legend((plot1, plot2, plot5), ('Empirical Dist', 'Probability Dist', 'Least-Squares of CCDF'))
plt.xlabel("Sample")
plt.ylabel("Frequency")
plt.xscale('log')
plt.yscale('log')
plt.savefig('ccdf.pdf')
plt.close()

# Problem 2.5
alpha = sum(np.log(np.array(keys)) * np.array(freqs)) + 1
print alpha
yfit4 = [t ** (-alpha) for t in x]

plot1, = plt.plot(keys, freqs, color = '#fa6e59')
plot2, = plt.plot(x, y, color = '#5294b1')
plot6, = plt.plot(x, yfit4, color = '#9a3159')
plt.title("Distributions and Estimation")
plt.legend((plot1, plot2, plot5), ('Empirical Dist', 'Probability Dist', 'MLE Estimator'))
plt.xlabel("Sample")
plt.ylabel("Frequency")
plt.xscale('log')
plt.yscale('log')
plt.savefig('mle.pdf')
plt.close()

# Problem 2.6
lspdf = []
lspdfprime = []
lsccdf = []
mle = []
for _ in xrange(100):
    samples = {}
    for _ in xrange(100000):
        u = random.random()
        sample = round(1/u)
        if sample not in samples.keys():
            samples[sample] = 1
        else:
            samples[sample] += 1

    pairs = sorted(samples.items(), key = lambda x: x[0])
    keys = []
    freqs = []
    for k, v in pairs:
        keys.append(k)
        freqs.append(v / 100000.0)
    x1 = np.log(np.array(keys))
    y1 = np.log(np.array(freqs))
    A = np.vstack([x1, np.ones(len(x1))]).T
    slope, intercept = np.linalg.lstsq(A, y1)[0]
    lspdf.append(-slope)
    x2 = np.log(np.array([k for k in keys if k <= 100]))
    y2 = np.log(np.array(freqs[0:len(x2)]))
    A = np.vstack([x2, np.ones(len(x2))]).T
    slope, intercept = np.linalg.lstsq(A, y2)[0]
    lspdfprime.append(-slope)
    x3 = np.log(np.array(keys))
    y3 = np.log(np.array([sum(freqs[0:k+1]) for k in xrange(len(freqs))]))
    A = np.vstack([x3, np.ones(len(x3))]).T
    slope, intercept = np.linalg.lstsq(A, y3)[0]
    lsccdf.append(1-slope)
    alpha = sum(np.log(np.array(keys)) * np.array(freqs)) + 1
    mle.append(alpha)

print sum(lspdf) / 100, np.std(np.array(lspdf))
print sum(lspdfprime) / 100, np.std(np.array(lspdfprime))
print sum(lsccdf) / 100, np.std(np.array(lsccdf))
print sum(mle) / 100, np.std(np.array(mle))
