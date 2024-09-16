import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random

def generate_unit_vector():
    phi = np.random.uniform(0, np.pi * 2)
    costheta = np.random.uniform(-1, 1)
    theta = np.arccos(costheta)  # Correct function np.arccos
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    return np.array([x, y, z])

def generate_chain(N):
    segments = [generate_unit_vector() for _ in range(N)]
    positions = np.cumsum(segments, axis=0)
    return positions

def compute_h2(chains):
    return np.mean([np.dot(chain[-1], chain[-endi]) for chain in chains])

def plot_chains(chains, N):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    for chain in chains:
        ax.plot(chain[:, 0], chain[:, 1], chain[:, 2])
    plt.title(f'3D Conformations for N={N}')
    plt.savefig(f'Chain3D{N}.png')
    plt.close()

# Select values for N
Ns = [10, 50, 100, 200, 400]
h2_values = []

for N in Ns:
    chains = [generate_chain(N) for _ in range(2000)]
    h2 = compute_h2(chains)
    h2_values.append(h2)
    
    # Select 50 random chains and plot
    selected_chains = random.sample(chains, 50)
    plot_chains(selected_chains, N)

# Plot h2 vs N
plt.figure(figsize=(8, 6))
plt.plot(Ns, h2_values, marker='o')
plt.title('Mean Squared End-to-End Distance $h^2(N)$ vs $N$')
plt.xlabel('$N$ (Number of segments)')
plt.ylabel('$h^2(N)$')
plt.grid(True)
plt.savefig('h2vsN.png')
plt.close()

# Estimate the scaling relationship v, where h2(N) \propto N^v
v, intercept = np.polyfit(np.log(Ns), np.log(h2_values), 1)
print(f"Estimated scaling exponent v: {v}")
