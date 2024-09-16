import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random

# Function to generate a random 3D unit vector
def random_unit_vector():
    phi = np.random.uniform(0, np.pi * 2)
    costheta = np.random.uniform(-1, 1)
    sintheta = np.sqrt(1 - costheta**2)
    x = sintheta * np.cos(phi)
    y = sintheta * np.sin(phi)
    z = costheta
    return np.array([x, y, z])

# Function to generate one polymer chain
def generate_polymer_chain(N):
    segments = [random_unit_vector() for _ in range(N)]
    positions = np.cumsum(segments, axis=0)
    return positions

# Function to calculate mean squared end-to-end distance
def calculate_h2(chains):
    distances = [np.sum((chain[-1] - chain[0])**2) for chain in chains]
    mean_h1 = np.mean(distances)
    return mean_h1

# Main simulation parameters
Ns = [10, 50, 100, 200, 400]
num_chains = 2000
sample_size = 50

# Storage for results
mean_h2_values = []
all_chains_for_plotting = {}

# Generate and analyze chains for each N
for N in Ns:
    chains = [generate_polymer_chain(N) for _ in range(num_chains)]
    mean_h2 = calculate_h2(chains)
    mean_h2_values.append(mean_h2)
    selected_chains = random.sample(chains, sample_size)
    all_chains_for_plotting[N] = selected_chains

    # Plotting the selected chains
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for chain in selected_chains:
        ax.plot(chain[:, 0], chain[:, 1], chain[:, 2], linewidth=1)
    ax.set_title(f'Polymer Chain Configurations for N={N}')
    plt.savefig(f'Chain3D{N}.png')
    plt.close()

# Plotting h2 vs. N
plt.figure()
plt.loglog(Ns, mean_h2_values, 'o-', color='blue')
plt.xlabel('Number of Segments (N)')
plt.ylabel('Mean Squared End-to-End Distance (h2)')
plt.title('Scaling of h2 with Polymer Chain Length')
plt.grid(True)
plt.savefig('h2vsN.png')
plt.close()

# Estimating the scaling exponent v
coeffs = np.polyfit(np.log(Ns), np.log(mean_h2_values), 1)
v = coeffs[0]
print(f"Scaling exponent v: {v:.4f}")
