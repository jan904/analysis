import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter

with open('Telepix.txt', 'r') as f:
    data = np.loadtxt(f, dtype = str, usecols = 0, delimiter=',')
    data = [int(i) for i in data]

freq = 12e6

def calibration(data):
    max_bin = np.max(data)
    counts = pd.Series(data).value_counts()
    entries = len(data)
    bins = []
    for i in range(max_bin+1):
        try:
            bins.append((counts.get(i)/entries) * 1/freq)
        except:
            bins.append(0)

    timestamps = np.cumsum(bins) #- np.array(bins)/2

    return timestamps

def delta_T(timestamps_1, timestamps_2, offset = 0):

    which_first = -1
    delta_T = []

    if which_first > 0:
        for time_1, time_2 in zip(timestamps_1, timestamps_2):
            if time_1 < time_2:
               delta_T.append(1/freq - time_2 + time_1)
            else:
              delta_T.append(time_1 - time_2)
    else:
        for time_1, time_2 in zip(timestamps_1, timestamps_2):
            if time_1 > time_2:    
                delta_T.append(1/freq - time_1 + time_2)
            else:    
                delta_T.append(time_2 - time_1)
    
    delta_T = np.array(delta_T) 

    return delta_T - offset

def find_zero(calibration_file):

    with open(calibration_file, 'r') as f:
        data = np.loadtxt(f, dtype = str, usecols = 0, delimiter=',')
        data = [int(i) for i in data]

    first = data[:-1:2]
    second = data[1::2]
    calibration_1 = calibration(first)
    calibration_2 = calibration(second)
    times_1 = calibration_1[first]
    times_2 = calibration_2[second]
    delta_t = delta_T(times_1, times_2, 0) 

    occurence_count = Counter(delta_t)

    return occurence_count.most_common(1)[0][0]

offset_zero = 0 #find_zero('delta_T_0Grad_500MHz.txt') #- 1/freq
print(offset_zero)

first = data[:-1:2]
second = data[1::2]

calibration_1 = calibration(first)
calibration_2 = calibration(second)

times_1 = calibration_1[first]
times_2 = calibration_2[second]
delta_t = np.array(delta_T(times_1, times_2, offset_zero)) * 1e9  

plt.hist(delta_t, bins = 83, range = (0,83))
plt.xlabel('Delta T [ns]')
plt.ylabel('Entries')
plt.title('Distribution of Delta T')
plt.show()






