import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def generate_random_unit_vector():
    phi = np.random.uniform(0, 2 * np.pi)
    costheta = np.random.uniform(-1, 1)
    theta = np.arccos(costheta)
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    return np.array([x, y, z])

def generate_polymer_chain(N):
    chain = np.zeros((N + 1, 3))
    for i in range(1, N + 1):
        chain[i] = chain[i-1] + generate_random_unit_vector()
    return chain

def calculate_h2(chains):
    end_to_end = chains[:, -1, :] - chains[:, 0, :]
    return np.mean(np.sum(end_to_end**2, axis=1))

def plot_chains(chains, N):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    for chain in chains:
        ax.plot(chain[:, 0], chain[:, 1], chain[:, 2])
    ax.set_title(f"3D Polymer Chains (N={N})")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.savefig(f"Chain3D{N}.png")
    plt.close()

N_values = [10, 50, 100, 200]
num_chains = 2000
h2_values = []

for N in N_values:
    chains = np.array([generate_polymer_chain(N) for _ in range(num_chains)])
    h2 = calculate_h2(chains)
    h2_values.append(h2)
    
    # Plot 50 random chain conformations
    random_chains = chains[np.random.choice(num_chains, 50, replace=False)]
    plot_chains(random_chains, N)

# Plot h2(N) vs N
plt.figure(figsize=(10, 6))
plt.plot(N_values, h2_values, 'bo-')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('N')
plt.ylabel('h2(N)')
plt.title('Mean Squared End-to-End Distance vs. Number of Segments')
plt.savefig('h2vsN.png')
plt.close()

# Determine scaling relationship
log_N = np.log(N_values)
log_h2 = np.log(h2_values)
v, _ = np.polyfit(log_N, log_h2, 1)

print(f"Scaling exponent v: {v:.4f}")
