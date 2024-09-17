import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Paths to the data and plot files
distance_data_path = 'distance_data.txt'
predictions_path = 'collision_predictions.txt'

# Define critical threshold in kilometers
CRITICAL_DISTANCE_KM = 1e6
day_to_s = 86400  # Number of seconds in a day

# Load the distance data file
try:
    data = np.loadtxt(distance_data_path, skiprows=1)
    time_array = data[:, 0]
    distance_data = data[:, 1]
except Exception as e:
    print(f"Error loading distance data: {e}")
    raise

# Load previous predictions
try:
    with open(predictions_path, 'r') as file:
        old_predictions = file.readlines()
except Exception as e:
    print(f"Error loading predictions: {e}")
    raise

# Compute new statistics based on extended data
new_min_distance = np.min(distance_data)
new_max_distance = np.max(distance_data)
new_avg_distance = np.mean(distance_data)
new_std_distance = np.std(distance_data)
new_min_dist_time = time_array[np.argmin(distance_data)]
new_max_dist_time = time_array[np.argmax(distance_data)]

new_min_dist_date = datetime(2024, 1, 1) + timedelta(seconds=new_min_dist_time)
new_max_dist_date = datetime(2024, 1, 1) + timedelta(seconds=new_max_dist_time)

# Print new statistics to verify the data load correctly
print(f"New Minimum Distance: {new_min_distance:.2f} km at {new_min_dist_date}")
print(f"New Maximum Distance: {new_max_distance:.2f} km at {new_max_dist_date}")
print(f"New Average Distance: {new_avg_distance:.2f} km")
print(f"New Standard Deviation of Distances: {new_std_distance:.2f} km")

# Generate new predictions and alerts
new_alerts = []
below_critical_indices = np.where(distance_data < CRITICAL_DISTANCE_KM)[0]
below_critical_dates = []

if below_critical_indices.size > 0:
    print("ALERT: Asteroid is within the critical distance threshold of Earth at new points during the year.")
    below_critical_times = time_array[below_critical_indices]
    below_critical_dates = [datetime(2024, 1, 1) + timedelta(seconds=t) for t in below_critical_times]
    new_alerts = [f"New critical distance threshold surpassed on: {date}" for date in below_critical_dates]

new_predictions = []
for i, date in enumerate(below_critical_dates):
    new_predictions.append(f"New potential close approach on: {date}. Predicted minimum distance: {distance_data[below_critical_indices[i]]:.2f} km")

# Save new predictions to a file
new_predictions_path = 'new_collision_predictions.txt'
with open(new_predictions_path, 'w') as f:
    for prediction in new_predictions:
        f.write(prediction + '\n')

# Print new predictions
for prediction in new_predictions:
    print(prediction)

# Enhanced Plot based on new predictions - comparing orbits to critical thresholds
plt.figure(figsize=(10, 6))
plt.plot(time_array / day_to_s, distance_data, label='Distance (km)')
plt.axhline(y=CRITICAL_DISTANCE_KM, color='r', linestyle='--', label='Critical Distance Threshold')
plt.scatter(time_array[below_critical_indices] / day_to_s, distance_data[below_critical_indices], c='r', marker='x', label='Threshold Surpasses')
plt.title('Asteroid Close Approaches and Critical Thresholds (Extended)')
plt.xlabel('Time (days)')
plt.ylabel('Distance (km)')
plt.legend()
plt.savefig('new_collision_prediction_plot.png')
plt.show()

print("Extended collision predictions and critical alerts completed and saved.")
