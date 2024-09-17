from skyfield.api import load
import numpy as np
import matplotlib.pyplot as plt

# Constants
G = 6.67430e-11  # Gravitational constant in m^3/kg/s^2
AU_to_km = 1.496e+8  # 1 AU in kilometers
km_to_m = 1e3
day_to_s = 86400
half_hour_to_s = 1800
year_to_s = 365.25 * day_to_s

# Load planetary data
eph = load('de421.bsp')
sun = eph['sun']
earth = eph['earth']
moon = eph['moon']
mars = eph['mars']
ts = load.timescale()
time = ts.utc(2024, 1, 1, 0, 0, 0)

# Get initial positions and velocities
def get_body_data(body):
    position = body.at(time).position.km  # km
    velocity = body.at(time).velocity.km_per_s  # km/s
    return position, velocity

bodies = {
    'sun': (sun, 1.989e30),
    'earth': (earth, 5.972e24),
    'moon': (moon, 7.348e22),
    'mars': (mars, 6.417e23)
}

initial_data = {}
for name, (body, mass) in bodies.items():
    position, velocity = get_body_data(body)
    initial_data[name] = {'position': np.array(position), 'velocity': np.array(velocity), 'mass': mass}
    print(f"{name.capitalize()} - Position: {position} km, Velocity: {velocity} km/s, Mass: {mass} kg")

# Initial condition for the asteroid
earth_position = initial_data['earth']['position']
earth_velocity = initial_data['earth']['velocity']
d_ast = 6e8  # km
v_ast = 20  # km/s
angle_away_from_xy = np.radians(15)  # in radians

asteroid_position = earth_position + d_ast * np.array([1, 0, 0])
asteroid_velocity = earth_velocity + v_ast * np.array([np.cos(angle_away_from_xy), 0, np.sin(angle_away_from_xy)])  # km/s

diameter = 50  # meters
density = 2.5  # g/cm^3 -> kg/m^3
volume = (4/3) * np.pi * (diameter / 2)**3  # m^3
mass_asteroid = volume * density * 1000  # kg

initial_data['asteroid'] = {
    'position': asteroid_position,
    'velocity': asteroid_velocity,
    'mass': mass_asteroid
}
print(f"Asteroid - Position: {asteroid_position} km, Velocity: {asteroid_velocity} km/s, Mass: {mass_asteroid} kg")

# Time array
simulation_duration = year_to_s  # seconds
time_steps = int(simulation_duration / half_hour_to_s)
time_array = np.linspace(0, simulation_duration, time_steps)

# Arrays to store the trajectories
trajectories = {name: {'position': [], 'velocity': []} for name in initial_data.keys()}

# Initial conditions
for name in initial_data.keys():
    trajectories[name]['position'].append(initial_data[name]['position'])
    trajectories[name]['velocity'].append(initial_data[name]['velocity'])

# Function to compute gravitational force
def gravitational_force(m1, m2, r):
    r_m = r * km_to_m  # Convert distance to meters
    force_magnitude = (G * m1 * m2) / np.linalg.norm(r_m)**2
    force_direction = r_m / np.linalg.norm(r_m)
    force = force_magnitude * force_direction  # Force in Newtons
    return force / km_to_m  # Convert force back to km/s^2

# Runge-Kutta 4th Order Method
def rk4_step(name, dt):
    pos = np.array(trajectories[name]['position'][-1])  # km
    vel = np.array(trajectories[name]['velocity'][-1])  # km/s
    
    k1v = dt * acceleration(name, pos)
    k1x = dt * (vel * km_to_m)  # to m/s
    
    k2v = dt * acceleration(name, pos + 0.5 * k1x / km_to_m)
    k2x = dt * ((vel + 0.5 * k1v) * km_to_m)
    
    k3v = dt * acceleration(name, pos + 0.5 * k2x / km_to_m)
    k3x = dt * ((vel + 0.5 * k2v) * km_to_m)
    
    k4v = dt * acceleration(name, pos + k3x / km_to_m)
    k4x = dt * ((vel + k3v) * km_to_m)

    new_vel = vel + (1/6) * (k1v + 2 * k2v + 2 * k3v + k4v)
    new_pos = pos + (1/6) * (k1x + 2 * k2x + 2 * k3x + k4x) / km_to_m
    
    return new_pos, new_vel

# Compute acceleration
def acceleration(name, pos):
    acc = np.array([0.0, 0.0, 0.0])
    for other_name in [other for other in initial_data if other != name]:
        other_pos = np.array(trajectories[other_name]['position'][-1])
        r = other_pos - pos
        m1 = initial_data[name]['mass']
        m2 = initial_data[other_name]['mass']
        acc += gravitational_force(m2, m1, r) / m1  # km/s^2 (converted m/s^2 to km/s^2)
    return acc

# Run the simulation
for t in range(1, time_steps):
    for name in initial_data.keys():
        new_pos, new_vel = rk4_step(name, half_hour_to_s)
        trajectories[name]['position'].append(new_pos)
        trajectories[name]['velocity'].append(new_vel)

# Extract positions for plotting
earth_positions = np.array(trajectories['earth']['position'])
mars_positions = np.array(trajectories['mars']['position'])
asteroid_positions = np.array(trajectories['asteroid']['position'])

# Save the distance data
distances = np.linalg.norm(earth_positions - asteroid_positions, axis=1)
np.savetxt('distance_data.txt', np.column_stack((time_array, distances)), header='Time(s) Distance(km)')

# Plotting
fig, axs = plt.subplots(3, 1, figsize=(8, 12))

# Plot x-y plane
axs[0].plot(earth_positions[:, 0], earth_positions[:, 1], label='Earth')
axs[0].plot(mars_positions[:, 0], mars_positions[:, 1], label='Mars')
axs[0].plot(asteroid_positions[:, 0], asteroid_positions[:, 1], label='Asteroid')
axs[0].set_title('x-y plane')
axs[0].set_xlabel('x [km]')
axs[0].set_ylabel('y [km]')
axs[0].legend()

# Plot x-z plane
axs[1].plot(earth_positions[:, 0], earth_positions[:, 2], label='Earth')
axs[1].plot(mars_positions[:, 0], mars_positions[:, 2], label='Mars')
axs[1].plot(asteroid_positions[:, 0], asteroid_positions[:, 2], label='Asteroid')
axs[1].set_title('x-z plane')
axs[1].set_xlabel('x [km]')
axs[1].set_ylabel('z [km]')
axs[1].legend()

# Plot y-z plane
axs[2].plot(earth_positions[:, 1], earth_positions[:, 2], label='Earth')
axs[2].plot(mars_positions[:, 1], mars_positions[:, 2], label='Mars')
axs[2].plot(asteroid_positions[:, 1], asteroid_positions[:, 2], label='Asteroid')
axs[2].set_title('y-z plane')
axs[2].set_xlabel('y [km]')
axs[2].set_ylabel('z [km]')
axs[2].legend()

plt.tight_layout()
plt.savefig('orbit.png')

plt.figure()
plt.plot(time_array, distances)
plt.title('Distance between Earth and Asteroid')
plt.xlabel('Time [s]')
plt.ylabel('Distance [km]')
plt.savefig('distance.png')

print("Simulation completed, distance data saved, and plots saved.")
