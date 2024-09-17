import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Paths to the data and plot files
distance_data_path = 'distance_data.txt'
orbit_plot_path = 'orbit.png'
distance_plot_path = 'distance.png'

# Define the critical threshold in kilometers
CRITICAL_DISTANCE_KM = 1e6

# Load the distance data from a text file
# Assuming 'distance_data.txt' has two columns: time (seconds) and distance (kilometers)
data = np.loadtxt(distance_data_path, skiprows=1)
time_array = data[:, 0]
distance_data = data[:, 1]

# Compute statistics
min_distance = np.min(distance_data)
max_distance = np.max(distance_data)
avg_distance = np.mean(distance_data)
std_distance = np.std(distance_data)
min_dist_time = time_array[np.argmin(distance_data)]
max_dist_time = time_array[np.argmax(distance_data)]

# Calculate the dates for the min and max distances
start_date = datetime(2024, 1, 1)
min_dist_date = start_date + timedelta(seconds=min_dist_time)
max_dist_date = start_date + timedelta(seconds=max_dist_time)

# Print statistics
print(f"Minimum Distance: {min_distance:.2f} km at {min_dist_date}")
print(f"Maximum Distance: {max_distance:.2f} km at {max_dist_date}")
print(f"Average Distance: {avg_distance:.2f} km")
print(f"Standard Deviation of Distances: {std_distance:.2f} km")

# Check if there are any critical threshold alerts
below_critical_indices = np.where(distance_data < CRITICAL_DISTANCE_KM)[0]
if below_critical_indices.size > 0:
    print("ALERT: Asteroid is within the critical distance threshold of Earth at some points during the year.")
    below_critical_times = time_array[below_critical_indices]
    below_critical_dates = [start_date + timedelta(seconds=t) for t in below_critical_times]
    for date in below_critical_dates:
        print(f"Critical distance threshold surpassed on: {date}")

# Save the analysis results to a text file
with open("distance_analysis.txt", "w") as file:
    file.write(f"Minimum Distance: {min_distance:.2f} km at {min_dist_date}\n")
    file.write(f"Maximum Distance: {max_distance:.2f} km at {max_dist_date}\n")
    file.write(f"Average Distance: {avg_distance:.2f} km\n")
    file.write(f"Standard Deviation of Distances: {std_distance:.2f} km\n")
    if below_critical_indices.size > 0:
        file.write("ALERT: Asteroid is within the critical distance threshold of Earth at some points during the year.\n")
        for date in below_critical_dates:
            file.write(f"Critical distance threshold surpassed on: {date}\n")

# Display the orbit plot
img_orbit = plt.imread(orbit_plot_path)
plt.figure(figsize=(10, 7))
plt.imshow(img_orbit)
plt.title('Orbital Paths of Earth, Mars, and Asteroid')
plt.axis('off')
plt.savefig('visualized_orbit.png')
plt.show()

# Summary report generation
with open('summary_report.txt', 'w') as file:
    file.write("Summary Report: Orbital Simulation Analysis\n")
    file.write("============================================\n\n")
    file.write(f"Minimum Distance between Earth and Asteroid: {min_distance:.2f} km at {min_dist_date}\n")
    file.write(f"Maximum Distance between Earth and Asteroid: {max_distance:.2f} km at {max_dist_date}\n")
    file.write(f"Average Distance between Earth and Asteroid: {avg_distance:.2f} km\n")
    file.write(f"Standard Deviation of Distances: {std_distance:.2f} km\n\n")
    if below_critical_indices.size > 0:
        file.write("ALERT: The Asteroid is within the critical distance threshold of Earth at certain points during the year.\n")
        for date in below_critical_dates:
            file.write(f"Critical distance threshold surpassed on: {date}\n")
print("Summary report generated.")
