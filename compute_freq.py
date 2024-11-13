import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.stats import norm


full_data = []
skiprows_next : int = 0
fine : list = []
coarse : list = []
coarse_bin : str = ''
freq : list = []
diff : list = []

def get_data(skiprows : int) -> list[int]:
    with open('output_dec.txt', 'r') as f:
        data = np.loadtxt(f, dtype = str, usecols = 0, delimiter=',', max_rows = 10000, skiprows = skiprows)
        data = [int(i) for i in data]                            
    return data

def dec_to_bin(dec : int) -> str:
    binary = int(bin(dec)[2:])
    while len(str(binary)) < 8:
        binary = '0' + str(binary)
    return binary


while (get_data(skiprows_next) != []):
    data = get_data(skiprows_next)
    full_data.extend(data)
    skiprows_next += 10000

for i in range(0, len(full_data)-3, 5):
    if full_data[i] > 127:
        fine.append(0)
    else:
        fine.append(full_data[i])
    coarse_bin = str(dec_to_bin(full_data[i+4])) + str(dec_to_bin(full_data[i+3])) + str(dec_to_bin(full_data[i+2])) + str(dec_to_bin(full_data[i+1]))
    coarse.append(int(coarse_bin, 2))


for i in range(0, len(coarse)-1):
    diff.append(coarse[i+1] - coarse[i])

#diff = [d for d in diff if d == 239999]

for coarse_t, fine_t in zip(diff, fine):
    time = coarse_t * 1/(12 * 10**6) + fine_t * 765 * 10**-12
    if 1/time > 0:
        freq.append(1/time)

print(min(freq))
# Fit Gaussian curve to the histogram
mu, std = norm.fit(freq)

# Generate x values for the curve
#x = np.linspace(min(freq), max(freq), 100)

# Calculate y values for the curve
#y = norm.pdf(x, mu, std)

# Plot the histogram and the fitted Gaussian curve
fig, ax = plt.subplots()
ax.set_title('Frequency distribution')
ax.set_xlabel('Frequency [Hz]')
ax.set_ylabel('Bin frequency')
ax.set_xlim(50-5e-5,50+3e-4)
ax.hist(freq, density=True, bins = 50, range = (50-5e-5,50+3e-4))  # Set density=True to normalize the histogram
#ax.plot(x, y, 'r-', label= f'Gaussian Fit, mu = {mu:.7e}, std = {std:.2e}')
ax.legend()

plt.show()


fig, ax = plt.subplots()
ax.set_title('Bin frequency')
ax.set_xlabel('bins')
ax.set_ylabel('frequency')
ax.hist(fine, bins = 128, range = (0, 128))

plt.show()