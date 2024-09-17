import numpy as np
import matplotlib.pyplot as plt
from skyfield.api import load
from skyfield.constants import GM_SUN
from scipy.optimize import curve_fit

# Constants
G = 6.67430e-20  # km^3 kg^-1 s^-2
beta_values = [1, 1.001]
dt = 1800  # Time step in seconds (half an hour)
days = 700  # Simulation duration in days
total_steps = int(days * 86400 / dt)  # Total number of steps

# Load planetary data
ephemeris = load('de421.bsp')
sun = ephemeris['sun']
earth = ephemeris['earth']
moon = ephemeris['moon']
planets = ['mercury', 'venus', 'earth', 'mars']
planets_data = {planet: ephemeris[planet + ' barycenter'] for planet in planets}

# Get initial positions, velocities, and masses
ts = load.timescale()
t = ts.utc(2024, 1, 1, 0, 0, 0)
initial_positions = {}
initial_velocities = {}
masses = {
    "sun": 1.989e30,  # kg
    "mercury": 3.3011e23,  # kg
    "venus": 4.8675e24,  # kg
    "earth": 5.97237e24,  # kg
    "mars": 6.4171e23,  # kg
    "moon": 7.342e22   # kg
}

for planet, planet_obj in planets_data.items():
    astrometric = planet_obj.at(t)
    initial_positions[planet] = astrometric.position.km
    initial_velocities[planet] = astrometric.velocity.km_per_s

initial_positions['sun'] = sun.at(t).position.km
initial_velocities['sun'] = sun.at(t).velocity.km_per_s

initial_positions['moon'] = moon.at(t).position.km
initial_velocities['moon'] = moon.at(t).velocity.km_per_s

# Prepare arrays for positions and velocities
def initialize_arrays(num_objects, num_steps):
    positions = np.zeros((num_objects, num_steps, 3))
    velocities = np.zeros((num_objects, num_steps, 3))
    return positions, velocities

positions, velocities = initialize_arrays(len(planets_data) + 2, total_steps)
all_objects = ['sun', 'mercury', 'venus', 'earth', 'mars', 'moon']
for i, obj in enumerate(all_objects):
    positions[i, 0] = initial_positions[obj]
    velocities[i, 0] = initial_velocities[obj]

# Runge-Kutta 4th order method for numerical integration
def rk4_step(pos, vel, masses, beta, dt):
    def gravitational_acceleration(pos, masses, beta):
        acc = np.zeros_like(pos)
        for i in range(len(pos)):
            for j in range(len(pos)):
                if i != j:
                    r_vec = pos[j] - pos[i]
                    r = np.linalg.norm(r_vec)
                    r_unit = r_vec / r
                    acc[i] += G * masses[j] / r**(beta + 1) * r_unit
        return acc

    k1v = dt * gravitational_acceleration(pos, masses, beta)
    k1x = dt * vel

    k2v = dt * gravitational_acceleration(pos + 0.5 * k1x, masses, beta)
    k2x = dt * (vel + 0.5 * k1v)

    k3v = dt * gravitational_acceleration(pos + 0.5 * k2x, masses, beta)
    k3x = dt * (vel + 0.5 * k2v)

    k4v = dt * gravitational_acceleration(pos + k3x, masses, beta)
    k4x = dt * (vel + k3v)

    new_pos = pos + (k1x + 2*k2x + 2*k3x + k4x) / 6
    new_vel = vel + (k1v + 2*k2v + 2*k3v + k4v) / 6

    return new_pos, new_vel

# Run the simulation
def simulate_motion(beta, positions, velocities, masses):
    num_objects = len(positions)
    for step in range(1, total_steps):
        positions[:, step], velocities[:, step] = rk4_step(
            positions[:, step-1], velocities[:, step-1], masses, beta, dt
        )
    return positions, velocities

# Perform simulations for both beta values
results = {}
for beta in beta_values:
    pos, vel = initialize_arrays(len(planets_data) + 2, total_steps)
    for i, obj in enumerate(all_objects):
        pos[i, 0] = initial_positions[obj]
        vel[i, 0] = initial_velocities[obj]
    pos, vel = simulate_motion(beta, pos, vel, masses)
    results[beta] = pos

# Fit Earth's orbit using an ellipse formula
def ellipse_func(t, a, b, T, phi):
    return a * np.cos(2 * np.pi * t / T + phi), b * np.sin(2 * np.pi * t / T + phi)

def fit_ellipse(t_data, x_data, y_data):
    popt, _ = curve_fit(lambda t, a, b, T, phi: ellipse_func(t, a, b, T, phi)[0], t_data, x_data)
    a, b, T, phi = popt
    return lambda t: ellipse_func(t, a, b, T, phi)

earth_fit_funcs = {}
for beta in beta_values:
    t_data = np.linspace(0, days * 86400, total_steps)
    x_data = results[beta][all_objects.index('earth'), :, 0]
    y_data = results[beta][all_objects.index('earth'), :, 1]
    earth_fit_funcs[beta] = fit_ellipse(t_data, x_data, y_data)

# Plot the orbits
fig, ax = plt.subplots(figsize=(10, 10))
color_map = { 'mercury': 'gray', 'venus': 'yellow', 'earth': 'blue', 'mars': 'red' }
linestyle_map = {beta_values[0]: '-', beta_values[1]: '--'}

for planet in planets:
    for beta in beta_values:
        pos = results[beta]
        ax.plot(pos[all_objects.index(planet), :, 0], pos[all_objects.index(planet), :, 1],
                color=color_map[planet], linestyle=linestyle_map[beta], label=f'{planet}-beta-{beta}')

ax.set_title('Projections of Orbits on Plane')
ax.set_xlabel('x (km)')
ax.set_ylabel('y (km)')
ax.legend(loc='upper right')
plt.grid()
plt.savefig('orbits.png')

# Print initial positions and velocities for verification
print("Initial Positions (in km):")
for obj, pos in initial_positions.items():
    print(f"{obj.capitalize()}: {pos}")

print("\nInitial Velocities (in km/s):")
for obj, vel in initial_velocities.items():
    print(f"{obj.capitalize()}: {vel}")

# Output the fitted ellipse formulas for Earth's orbit
for beta in beta_values:
    fitted_func = earth_fit_funcs[beta]
    print(f"\nFitted ellipse function for Earth with beta={beta}:")
    print(f"x(t), y(t) = {fitted_func.__doc__}")

plt.show()
