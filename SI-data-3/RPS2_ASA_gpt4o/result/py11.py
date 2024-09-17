import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Paths to the data and plot files
distance_data_path = 'distance_data.txt'
predictions_path = 'new_collision_predictions.txt'

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
    old_predictions = []

# Compute overall impact probabilities (simplified as 1/distance method)
impact_probabilities = 1.0 / distance_data

# Analysis for shorter periods of close approaches (in weeks)
close_approaches_idx = np.where(distance_data < CRITICAL_DISTANCE_KM * 10)[0]
periods = {}
for idx in close_approaches_idx:
    week_period = int(time_array[idx] // (7 * day_to_s)) * (7 * day_to_s)
    if week_period in periods:
        periods[week_period].append(distance_data[idx])
    else:
        periods[week_period] = [distance_data[idx]]

# Detailed Review for Weeks
detailed_reviews = []
for period in sorted(periods.keys()):
    start_time = period
    end_time = start_time + (7 * day_to_s)
    period_distances = periods[period]
    min_distance = min(period_distances)
    avg_distance = np.mean(period_distances)
    max_distance = max(period_distances)
    detailed_reviews.append((start_time, end_time, min_distance, avg_distance, max_distance))

# Generate Report
report_path = 'impact_probabilities_report.txt'
with open(report_path, 'w') as report_file:
    report_file.write("Impact Probabilities and Periods of Close Approaches:\n\n")
    report_file.write("Overall Impact Probabilities (1/distance method):\n\n")
    for t, prob in zip(time_array, impact_probabilities):
        report_file.write(f"Time: {datetime(2024, 1, 1) + timedelta(seconds=t)}, Probability: {prob:.6E}\n")
    report_file.write("\nDetailed Review of Close Approaches (weekly):\n\n")
    for review in detailed_reviews:
        start = datetime(2024, 1, 1) + timedelta(seconds=review[0])
        end = datetime(2024, 1, 1) + timedelta(seconds=review[1])
        report_file.write(f"Week starting {start} to {end}:\n")
        report_file.write(f"   Minimum Distance: {review[2]:.2f} km\n")
        report_file.write(f"   Average Distance: {review[3]:.2f} km\n")
        report_file.write(f"   Maximum Distance: {review[4]:.2f} km\n\n")

# Plot detailed review for a specific week - closest week
if detailed_reviews:
    closest_week = min(detailed_reviews, key=lambda x: x[2])
    start_time = closest_week[0]
    end_time = closest_week[1]
    week_idx = np.where((time_array >= start_time) & (time_array <= end_time))[0]
    week_time = time_array[week_idx]
    week_distance = distance_data[week_idx]

    plt.figure(figsize=(10, 6))
    plt.plot(week_time / day_to_s, week_distance, label='Distance (km)')
    plt.axhline(y=CRITICAL_DISTANCE_KM, color='r', linestyle='--', label='Critical Distance Threshold')
    plt.title('Detailed Review of Closest Week')
    plt.xlabel('Time (days since week start)')
    plt.ylabel('Distance (km)')
    plt.legend()
    plt.savefig('detailed_closest_week.png')
    plt.show()

print("Detailed impact probability report and specific close approach review generated.")
