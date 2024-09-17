import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Paths to the data and plot files
distance_data_path = 'distance_data.txt'
impact_probabilities_report_path = 'impact_probabilities_report.txt'

# Constants
CRITICAL_DISTANCE_KM = 1e6
day_to_s = 86400  # Number of seconds in a day
earth_radius_km = 6371  # Average radius of Earth in kilometers

# Load the distance data file
try:
    data = np.loadtxt(distance_data_path, skiprows=1)
    time_array = data[:, 0]
    distance_data = data[:, 1]
except Exception as e:
    print(f"Error loading distance data: {e}")
    raise

# Load impact probabilities from the report file
try:
    with open(impact_probabilities_report_path, 'r') as file:
        report_lines = file.readlines()
    probabilities = []
    time_stamps = []
    for line in report_lines:
        if "Time:" in line and "Probability:" in line:
            parts = line.split(",")
            time_part = parts[0].split(":")[1].strip() + ":" + parts[0].split(":")[2].strip()
            prob_part = parts[1].split(":")[1].strip()
            date_time = datetime.strptime(time_part, '%Y-%m-%d %H:%M:%S.%f')
            prob = float(prob_part)
            time_stamps.append(date_time)
            probabilities.append(prob)
except Exception as e:
    print(f"Error loading probabilities report: {e}")
    raise

# Verify data alignment
if len(time_stamps) != len(distance_data):
    raise ValueError("Mismatch between number of timestamps in probabilities report and number of distance entries")

# Compute potential impact zones based on probabilities and distance thresholds
impact_zones = []
for timestamp, prob, distance in zip(time_stamps, probabilities, distance_data):
    severity = "High" if distance < CRITICAL_DISTANCE_KM else "Low"
    zone = {"time": timestamp, "probability": prob, "distance": distance, "severity": severity}
    impact_zones.append(zone)

# Generate a consolidated impact severity report
severity_report_path = 'impact_severity_report.txt'
with open(severity_report_path, 'w') as report_file:
    report_file.write("Asteroid Impact Severity Report:\n\n")
    for zone in impact_zones:
        report_file.write(f"Time: {zone['time']} | Probability: {zone['probability']:.6E} | Distance: {zone['distance']:.2f} km | Severity: {zone['severity']}\n")

# Visualize impact probabilities and risk zones
plt.figure(figsize=(12, 6))
times = [zone['time'] for zone in impact_zones]
probabilities = [zone['probability'] for zone in impact_zones]
distances = [zone['distance'] for zone in impact_zones]
severities = [zone['severity'] for zone in impact_zones]

plt.plot(times, distances, label='Distance (km)', color='blue')
plt.axhline(y=earth_radius_km, color='green', linestyle='--', label='Earth Radius')
plt.axhline(y=CRITICAL_DISTANCE_KM, color='red', linestyle='--', label='Critical Distance Threshold')
plt.fill_between(times, 0, distances, where=np.array(severities) == 'High', color='red', alpha=0.3, label='High Severity Zone')
plt.title('Asteroid Impact Probabilities and Risk Zones')
plt.xlabel('Time')
plt.ylabel('Distance (km)')
plt.legend()
plt.tight_layout()
plt.savefig('impact_probabilities_and_risk_zones.png')
plt.show()

print("Impact severity report and risk zone visualization completed.")
