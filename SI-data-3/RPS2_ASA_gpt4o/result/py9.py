import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Paths to the data and plot files
distance_data_path = 'distance_data.txt'
combined_analysis_path = 'combined_analysis.txt'

# Define critical threshold in kilometers
CRITICAL_DISTANCE_KM = 1e6
day_to_s = 86400  # Number of seconds in a day

# Load the distance data
try:
    data = np.loadtxt(distance_data_path, skiprows=1)
    time_array = data[:, 0]
    distance_data = data[:, 1]
except Exception as e:
    print(f"Error loading distance data: {e}")
    raise

# Compute statistics
min_distance = np.min(distance_data)
max_distance = np.max(distance_data)
avg_distance = np.mean(distance_data)
std_distance = np.std(distance_data)
min_dist_time = time_array[np.argmin(distance_data)]
max_dist_time = time_array[np.argmax(distance_data)]

start_date = datetime(2024, 1, 1)
min_dist_date = start_date + timedelta(seconds=min_dist_time)
max_dist_date = start_date + timedelta(seconds=max_dist_time)

# Print statistics to verify the data load correctly
print(f"Minimum Distance: {min_distance:.2f} km at {min_dist_date}")
print(f"Maximum Distance: {max_distance:.2f} km at {max_dist_date}")
print(f"Average Distance: {avg_distance:.2f} km")
print(f"Standard Deviation of Distances: {std_distance:.2f} km")

# Check for critical thresholds
alerts = []
below_critical_indices = np.where(distance_data < CRITICAL_DISTANCE_KM)[0]
below_critical_dates = []  # Ensure that this variable is defined even if there are no alerts

if below_critical_indices.size > 0:
    print("ALERT: Asteroid is within the critical distance threshold of Earth at some points during the year.")
    below_critical_times = time_array[below_critical_indices]
    below_critical_dates = [start_date + timedelta(seconds=t) for t in below_critical_times]
    alerts = [f"Critical distance threshold surpassed on: {date}" for date in below_critical_dates]

# Predictions and Advisories
predictions = []
for i, date in enumerate(below_critical_dates):
    predictions.append(f"Potential close approach on: {date}. Predicted minimum distance: {distance_data[below_critical_indices[i]]:.2f} km")

# Save predictions to a file
predictions_path = 'collision_predictions.txt'
with open(predictions_path, 'w') as f:
    for prediction in predictions:
        f.write(prediction + '\n')

# Print predictions
for prediction in predictions:
    print(prediction)

# Plot based on predictions - comparing orbits to critical thresholds
plt.figure(figsize=(10, 6))
plt.plot(time_array / day_to_s, distance_data, label='Distance (km)')
plt.axhline(y=CRITICAL_DISTANCE_KM, color='r', linestyle='--', label='Critical Distance Threshold')
plt.scatter(time_array[below_critical_indices] / day_to_s, distance_data[below_critical_indices], c='r', marker='x', label='Critical Threshold Surpassed')
plt.title('Asteroid Close Approaches and Critical Thresholds')
plt.xlabel('Time (days)')
plt.ylabel('Distance (km)')
plt.legend()
plt.savefig('collision_prediction_plot.png')
plt.show()

print("Collision predictions and critical alerts completed and saved.")
