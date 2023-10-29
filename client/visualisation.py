import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import norm
from scipy import stats

domain = "google.com"
# network_condition = "1000kb throughput, 100ms latency, 20% packet loss no large files"
network_condition = "1 Mbps Bandwidth, Large files"

directory = "data/"

# Your data
http1_data = pd.read_csv(directory + "http1.1_"+domain+".csv")
http2_data = pd.read_csv(directory + "http2_"+domain+".csv")
http3_data = pd.read_csv(directory + "http3_"+domain+".csv")

# Convert the data to a Pandas DataFrame
data_http_1 = pd.DataFrame(http1_data, columns=["time_taken"])
data_http_2 = pd.DataFrame(http2_data, columns=["time_taken"])
data_http_3 = pd.DataFrame(http3_data, columns=["time_taken"])

# Define a function to remove outliers using the Z-score method
def remove_outliers_zscore(data, threshold=3):
    z_scores = np.abs(stats.zscore(data))
    filtered_data = data[(z_scores < threshold)]
    return filtered_data

# Remove outliers from both datasets
# data_http_1_filtered = remove_outliers_zscore(data_http_1)
# data_http_2_filtered = remove_outliers_zscore(data_http_2)
# data_http_3_filtered = remove_outliers_zscore(data_http_3)

data_http_1_filtered = data_http_1
data_http_2_filtered = data_http_2
data_http_3_filtered = data_http_3

# Determine the range for x-axis
x_min = min(data_http_1_filtered["time_taken"].min(), data_http_2_filtered["time_taken"].min(), data_http_3_filtered["time_taken"].min())
x_max = max(data_http_1_filtered["time_taken"].max(), data_http_2_filtered["time_taken"].max(), data_http_3_filtered["time_taken"].max())
margin = 0.2 * (x_max - x_min)  # 10% of the data range
x_range = np.linspace(x_min - margin, x_max + margin, 1000)

# Fit normal distribution to the filtered data
mu1, std1 = norm.fit(data_http_1_filtered)
mu2, std2 = norm.fit(data_http_2_filtered)
mu3, std3 = norm.fit(data_http_3_filtered)

# Calculate the probability density function (PDF) for the two distributions
pdf1 = norm.pdf(x_range, mu1, std1)
pdf2 = norm.pdf(x_range, mu2, std2)
pdf3 = norm.pdf(x_range, mu3, std3)

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(x_range, pdf1, label='http1', linestyle='--', color='green')
plt.plot(x_range, pdf2, label='http2', linestyle='--', color='blue')
plt.plot(x_range, pdf3, label='http3', linestyle='--', color='red')

# Plot the original data as a histogram
plt.hist(data_http_1_filtered, bins=20, density=True, alpha=0.5, color='green')
plt.hist(data_http_2_filtered, bins=20, density=True, alpha=0.5, color='blue')
plt.hist(data_http_3_filtered, bins=20, density=True, alpha=0.5, color='red')

iterations = len(data_http_1)

plt.xlabel('Time Taken')
plt.ylabel('Probability Density')
plt.title(f'Bell Curves for Time Taken for different HTTP Versions [{iterations} Iterations]', y=1.07)
plt.suptitle(f"Domain: {domain}; Network Conditions: {network_condition}", y=0.92, fontsize=10)
plt.grid(True)
plt.ylim(0, 100)

# Create a legend with mean and standard deviation information
legend_info = [
    f'http1: Mean={mu1:.2f}, Std={std1:.2f}',
    f'http2: Mean={mu2:.2f}, Std={std2:.2f}',
    f'http3: Mean={mu3:.2f}, Std={std3:.2f}'
]

plt.legend(legend_info)

# Show the plot
plt.savefig('output_figure.png')
