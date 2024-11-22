import numpy as np
import matplotlib.pyplot as plt
import ROOT

freq = 12e6
channels = ['00', '01', '10', '11']
timestamp = '2024-11-20_16:10:13'
all_bins = {channel: [] for channel in channels}
all_timestamps = {channel: [] for channel in channels}
all_data = {channel: [] for channel in channels}

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
        max_data = vals[-2]
        data = [int(i) if i != 288 else max_data for i in data]
        
        entries = len(data)
        bins = []
        vals, counts = np.unique(data, return_counts=True)

        # Fill in missing bins with 0
        full_range = np.arange(max_data)
        missing = np.setdiff1d(full_range, vals)
        for m in missing:
            counts = np.insert(counts, m, 0)
    
        for j in range(max_data + 1):
            bins.append((counts[j]/entries) * 1/freq)

        bins = np.array(bins) * 1e9
        timestamps = np.cumsum(bins)
        
        all_data[channel] = data
        all_bins[channel] = bins
        all_timestamps[channel] = timestamps
        
        plt.subplot(2, 2, i+1)
        plt.bar(range(max_data+1), bins, width=1, edgecolor = 'black', linewidth = .5, align='edge')
        plt.xlabel('Bins')
        plt.ylabel('Bin width [ns]')
        plt.title(f'Channel {int(channel, 2)}')
        
    plt.savefig(f'./data/{timestamp}/calibration.pdf', dpi=300)
    
    return all_data, all_bins, all_timestamps

def coincidence(timestamps, data, channels):
    
    times = {channel: [] for channel in channels}
    
    lens = [len(data[channel]) for channel in channels]
    for channel in channels:
        data[channel] = np.array(data[channel])
        data[channel] = data[channel][:min(lens)]
        timestamps[channel] = np.array(timestamps[channel])
        times[channel] = timestamps[channel][data[channel]]
    
    times['00'] = times['00'][1:]  
    times['01'] = times['01'][:-1]
    times['10'] = times['10'][:-1]
    times['11'] = times['11'][:-1]
      
    mean1 = np.mean([times['00'], times['01']], axis=0)
    mean2 = np.mean([times['10'], times['11']], axis=0)
    
    diff = mean1 - mean2
    mask = diff < 0
    diff[mask] = diff[mask] + 1/freq * 1e9
    
    mask = diff > 80
    diff[mask] = diff[mask] - 1/freq * 1e9
    
    mask = diff < 3
    diff = diff[mask]
    
    plot_hist(diff*1e3)
    
def plot_hist(data):
    range_ = [int(np.min(data)//100 * 100) - 50 ,int((np.max(data)) + 100)//100 * 100 + 50]
    length_ = int((range_[1] - range_[0])/100)

    hist = ROOT.TH1F('Statistics', 'Coincidence with mean', length_ + 2, range_[0] - 100, range_[1] + 100)
    
    for i in data:
        hist.Fill(i)
    hist.Scale(1/hist.Integral("width"))
    
    q_ = np.zeros(2)
    hist.GetQuantiles(2, q_, np.array([0.01, 0.99]))
    q0 = q_[0]
    q1 = q_[1]
    
    func = ROOT.TF1('func', 'ROOT::Math::normal_pdf(x, [0], [1])', q0, q1)   
    func.SetParameters(hist.GetRMS(), hist.GetMean())
    func.SetParNames('#sigma', '#mu')
    hist.Fit('func', 'Q')
    
    fit_max = func.GetMaximum() * 1.1
    
    hist.GetYaxis().SetRangeUser(0, fit_max)
    hist.GetXaxis().SetTitle('Time difference [ps]')
    hist.GetYaxis().SetTitle('Abundance')
    
    ROOT.gStyle.SetOptFit(1)
    ROOT.gStyle.SetOptStat(11)
    
    c = ROOT.TCanvas('c', 'c', 800, 600)
    hist.Draw("hist")
    func.Draw('same')
    c.SaveAs(f'./data/{timestamp}/fit.pdf')
    

data_, bins_, timestamps_ = plot_calib(timestamp, channels)
coincidence(timestamps_, data_, channels)

















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

