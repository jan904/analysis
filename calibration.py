import numpy as np
import matplotlib.pyplot as plt

freq = 12e6
channels = ['00', '01', '10', '11']
timestamp = '2024-11-20_16:10:13'
all_bins = {channel: [] for channel in channels}
all_timestamps = {channel: [] for channel in channels}

def get_data(directory, channel) -> list[int]:
    with open(f'./data/{directory}/{channel}.txt', 'r') as f:
        data = np.loadtxt(f, dtype = str, usecols = 0, delimiter=',')
        data = [int(i) for i in data]   
    return data


def plot_calib(dir, channels):
    plt.figure(figsize=(12, 12))
    for i, channel in enumerate(channels):
        data = get_data(timestamp, channel)

        vals, counts = np.unique(data, return_counts=True)
        
        entries = len(data)
        bins = []
        
        # Last value is the overflow currentlz
        max_bin = vals[-2]
        
        # Fill in missing bins with 0
        full_range = np.arange(max_bin)
        missing = np.setdiff1d(full_range, vals)
        for m in missing:
            counts = np.insert(counts, m, 0)
    
        for j in range(max_bin):
            bins.append((counts[j]/entries) * 1/freq)

        bins = np.array(bins) * 1e9
        timestamps = np.cumsum(bins)
        
        all_bins[channel] = bins
        all_timestamps[channel] = timestamps
        
        plt.subplot(2, 2, i+1)
        plt.bar(range(max_bin), bins, width=1, edgecolor = 'black', linewidth = .5, align='edge')
        plt.xlabel('Bins')
        plt.ylabel('Bin width [ns]')
        plt.title(f'Channel {int(channel, 2)}')
        
    plt.savefig(f'./data/{timestamp}/calibration.pdf', dpi=300)
    plt.show()

plot_calib(timestamp, channels)

















"""with open('single.txt', 'r') as f:
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
plt.show()"""

