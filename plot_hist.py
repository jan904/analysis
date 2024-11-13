import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.optimize import curve_fit


full_data = []
skiprows_next : int = 0


def const(x, c):
    return c

def get_data(skiprows : int) -> list[int]:
    with open('single.txt', 'r') as f:
        data = np.loadtxt(f, dtype = str, usecols = 0, max_rows = 1000, delimiter=',', skiprows = skiprows)
        data = [int(i) for i in data]                            
    return data


fig, ax = plt.subplots()
def update_hist(frame):

    error : int = 0
    total : int = 0
    fit : int = 0

    global skiprows_next
    data = get_data(skiprows_next)
    if len(data) < 1000:
        return
    full_data.extend(data)
    skiprows_next += 1000
    x = np.linspace(0, np.max(full_data)+1, 128)

    bins, edges = np.histogram(full_data, bins=128, range=(0, 128))
    popt, _ = curve_fit(const, edges[:-1], bins)

    total = np.sum(bins)
    fit = popt[0]/total
    
    #for bin in bins:
    #    bin = bin/total
    #    error += (bin - fit)**2

    ax.clear()
    ax.set_xlabel('bins')
    ax.set_ylabel('frequency')
    ax.hist(full_data, bins=128, range=(0, 128), width=1, edgecolor = 'black', linewidth = .5)
    ax.plot(x, popt[0] * np.ones(128), color='red', linestyle='-')
    ax.axvline(x=np.min(full_data), ymax=(popt[0]/(np.max(bins)*1.05)), color='red', linestyle='-')
    ax.axvline(x=np.max(full_data)+1, ymax=(popt[0]/(np.max(bins)*1.05)), color='red', linestyle='-')
    ax.set_title('Frequency distribution of the bins')
    ax.set_xlim(-2, np.max(full_data)+5)


ani = FuncAnimation(fig, update_hist, interval=.1)
plt.show()





