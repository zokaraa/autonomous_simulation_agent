import numpy as np
import matplotlib.pyplot as plt

# Define the critical threshold in kilometers
CRITICAL_DISTANCE_KM = 1e6

# Load the distance data from a text file
# Assuming 'distance_data.txt' has two columns: time (seconds) and distance (kilometers)
data = np.loadtxt('distance_data.txt')
time_array = data[:, 0]
distance_data = data[:, 1]

# Calculate minimum, maximum, and average distance
min_distance = np.min(distance_data)
max_distance = np.max(distance_data)
avg_distance = np.mean(distance_data)

# Find the times when the minimum and maximum distances occur
min_dist_time = time_array[np.argmin(distance_data)]
max_dist_time = time_array[np.argmax(distance_data)]

# Calculate the dates for the min and max distances
from datetime import datetime, timedelta

start_date = datetime(2024, 1, 1)
min_dist_date = start_date + timedelta(seconds=min_dist_time)
max_dist_date = start_date + timedelta(seconds=max_dist_time)

# Print the results
print(f"Minimum Distance between Earth and Asteroid: {min_distance} km at {min_dist_date}")
print(f"Maximum Distance between Earth and Asteroid: {max_distance} km at {max_dist_date}")
print(f"Average Distance between Earth and Asteroid: {avg_distance} km")

# Check if any distance falls below the critical threshold and alert
if np.any(distance_data < CRITICAL_DISTANCE_KM):
    print("ALERT: Asteroid is within the critical distance threshold of Earth at some points during the year.")

# Save the analysis results to a text file
with open("distance_analysis.txt", "w") as file:
    file.write(f"Minimum Distance: {min_distance} km at {min_dist_date}\n")
    file.write(f"Maximum Distance: {max_distance} km at {max_dist_date}\n")
    file.write(f"Average Distance: {avg_distance} km\n")
    if np.any(distance_data < CRITICAL_DISTANCE_KM):
        file.write("ALERT: Asteroid is within the critical distance threshold of Earth at some points during the year.\n")

print("Analysis completed and results saved to 'distance_analysis.txt'.")
