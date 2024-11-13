import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


with open('single.txt', 'r') as f:
    data = np.loadtxt(f, dtype = str, usecols = 0, delimiter=',')
    data = [int(i) for i in data]
    
freq = 12e6
max_bin = np.max(data)
counts = pd.Series(data).value_counts()
entries = len(data)
bins = []

for i in range(max_bin):
    bins.append((counts.get(i)/entries) * 1/freq)

timestamps = np.cumsum(bins)
timestamps = np.array([0] + list(timestamps))
print(data.count(0))
bins_ns = np.array(bins) * 1e9

mean_width = np.mean(bins_ns)

plt.bar(range(max_bin), bins_ns, width=1, edgecolor = 'black', linewidth = .5, align='edge')
plt.xlabel('Bins')
plt.ylabel('Bin width [ns]')
plt.title('Bin width in ns')
plt.legend([f'Entries = {entries} \n Max bin = {max_bin}'])
plt.savefig('bin_distr_single.png', dpi = 600)
plt.show()



plt.hist(bins_ns, range = (0.2, 1.7), bins = 30, edgecolor = 'black', linewidth = .5)
plt.xlabel('Bin width [ns]')
plt.ylabel('Entries')
plt.title('Distribution of bin widths')
plt.legend([f'Mean bin width = {mean_width:.3f} ns'])
plt.savefig('max1000_bin_distr.png', dpi = 600)
plt.show()


arrival_time = timestamps[data] * 1e9

plt.hist(arrival_time, bins = 20, edgecolor = 'black', linewidth = .5)
plt.xlabel('Arrival time [ns]')
plt.ylabel('Entries')
plt.title('Distribution of arrival times')
plt.show()

