import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Paths to the data and plot files
distance_data_path = 'distance_data.txt'
orbit_plot_path = 'orbit.png'

# Define critical threshold in kilometers
CRITICAL_DISTANCE_KM = 1e6
day_to_s = 86400  # Number of seconds in a day

# Load the distance data file
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

# Check if there are any critical threshold alerts and record
alerts = []
below_critical_indices = np.where(distance_data < CRITICAL_DISTANCE_KM)[0]
if below_critical_indices.size > 0:
    print("ALERT: Asteroid is within the critical distance threshold of Earth at some points during the year.")
    below_critical_times = time_array[below_critical_indices]
    below_critical_dates = [start_date + timedelta(seconds=t) for t in below_critical_times]
    alerts = [f"Critical distance threshold surpassed on: {date}" for date in below_critical_dates]

# Save the analysis results to a text file
with open("combined_analysis.txt", "w") as file:
    file.write(f"Minimum Distance: {min_distance:.2f} km at {min_dist_date}\n")
    file.write(f"Maximum Distance: {max_distance:.2f} km at {max_dist_date}\n")
    file.write(f"Average Distance: {avg_distance:.2f} km\n")
    file.write(f"Standard Deviation of Distances: {std_distance:.2f} km\n")
    if alerts:
        file.write("ALERT: Asteroid is within the critical distance threshold of Earth at some points during the year.\n")
        for alert in alerts:
            file.write(alert + "\n")

# Display and annotate the orbit plot
img_orbit = plt.imread(orbit_plot_path)
fig, ax = plt.subplots(figsize=(10, 7))
ax.imshow(img_orbit)
ax.set_title('Orbital Paths of Earth, Mars, and Asteroid')
ax.axis('off')
plt.savefig('annotated_orbit_paths.png')
plt.show()

# Superimpose distance plot
plt.figure(figsize=(10, 5))
plt.plot(time_array / day_to_s, distance_data, label='Distance (km)')
plt.axhline(y=CRITICAL_DISTANCE_KM, color='r', linestyle='--', label='Critical Distance Threshold')
plt.scatter(time_array / day_to_s, distance_data, c='b', s=1)
plt.title('Distance between Earth and Asteroid over Time')
plt.xlabel('Time (days)')
plt.ylabel('Distance (km)')
plt.legend()
plt.savefig('combined_distance_analysis.png')
plt.show()

# Save all resultant files with appropriate names
plt.figure(figsize=(12, 8))
img = plt.imread(orbit_plot_path)
plt.imshow(img)
plt.title('Superimposed Orbits with Distance Metrics')
plt.axis('off')
plt.tight_layout()
plt.savefig('superimposed_orbit_with_distances.png')
plt.show()

print("Analysis complete, images and data saved as specified.")
