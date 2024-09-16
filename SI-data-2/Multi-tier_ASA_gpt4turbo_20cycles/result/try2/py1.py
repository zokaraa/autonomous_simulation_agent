import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def generate_random_unit_vector():
    phi = np.random.uniform(0, np.pi * 2)
    costheta = np.random.uniform(-1, 1)
    sintheta = np.sqrt(1 - costheta**2)
    return np.array([sintheta * np.cos(phi), sintheta * np.sin(phi), costheta])

def generate_polymer_chain(N):
    # Start at origin
    positions = [np.array([0.0, 0.0, 0.0])]
    for _ in range(N):
        new_direction = generate_random_unit_vector()
        new_position = positions[-1] + new_direction
        positions.append(new_position)

    return np.array(positions)

def calculate_end_to_end_distance(chain):
    return np.linalg.norm(chain[0] - chain[-1])

N_values = [10, 50, 100, 200, 400]
num_chains = 2000
h2_values = []
chain_samples = {}

# Initialize dictionary to store sample chains for plotting
for N in N_values:
    chain_samples[N] = []

# Simulate chains and track mean squared distances
for N in N_values:
    distances = []
    for _ in range(num_chains):
        chain = generate_polymer_chain(N)
        distance = calculate_end_to_end_distance(chain)
        distances.append(distance**2)
        if len(chain_samples[N]) < 50:
            chain_samples[N].append(chain)
    mean_squared_distance = np.mean(distances)
    h2_values.append(mean_squared_distance)
    print(f'Mean squared end-to-end distance for N={N}: {mean_squared_distance}')

# Plot the chain samples
for N, samples in chain_samples.items():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for sample in samples:
        ax.plot(sample[:, 0], sample[:, 1], sample[:, 2])
    plt.title(f"Random Walks for N={N}")
    plt.savefig(f'Chain3D{N}.png')

# Plot h2(N) versus N
plt.figure()
plt.plot(N_values, h2_values, marker='o')
plt.xlabel('Number of segments (N)')
plt.ylabel('Mean squared end-to-end distance (h2(N))')
plt.title('h2(N) vs. N')
plt.savefig('h2vsN.png')

# Perform a linear regression to find the exponent v in h2(N) ~ N^v
log_N = np.log(N_values)
log_h2 = np.log(h2_values)
slope, intercept = np.polyfit(log_N, log_h2, 1)
print(f'Scaling exponent v: {slope}')
