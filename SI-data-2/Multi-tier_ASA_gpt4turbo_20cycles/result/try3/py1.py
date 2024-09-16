# Importing necessary libraries
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def generate_unit_vector():
    # Generating a random 3D unit vector
    phi = np.random.uniform(0, 2 * np.pi)
    theta = np.arccos(np.random.uniform(-1, 1))
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    return np.array([x, y, z])

def generate_polymer_chain(N):
    # Generating a polymer chain of length N
    positions = np.zeros((N, 3))
    for i in range(1, N):
        positions[i] = positions[i - 1] + generate_unit_vector()
    return positions

def calculate_h2(polymer_chains):
    # Calculating mean squared end-to-end distance
    N = polymer_chains.shape[1]
    h2 = np.mean(np.sum((polymer_chains[:, -1, :] - polymer_chains[:, 0, :]) ** 2, axis=1))
    return h2

def plot_polymer_chains(chains, N):
    # Plotting polymer chains in 3D
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    for chain in chains:
        ax.plot(chain[:, 0], chain[:, 1], chain[:, 2])
    ax.set_title(f'3D Random Walk for N={N}')
    plt.savefig(f'Chain3D{N}.png')
    plt.close()

def main():
    N_values = [10, 50, 100, 200, 400]
    h2_values = []
    
    for N in N_values:
        num_chains = 2000
        polymer_chains = np.array([generate_polymer_chain(N) for _ in range(num_chains)])
        h2 = calculate_h2(polymer_chains)
        h2_values.append(h2)
        sample_chains = polymer_chains[np.random.choice(num_chains, 50, replace=False)]
        plot_polymer_chains(sample_chains, N)
    
    # Plotting h2 vs N
    plt.figure()
    plt.plot(N_values, h2_values, 'o-')
    plt.xlabel('N (Number of segments)')
    plt.ylabel('Mean Squared End-to-End Distance, h2(N)')
    plt.title('Mean Squared End-to-End Distance vs. Number of Segments')
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(True)
    plt.savefig('h2vsN.png')
    plt.close()
    
    # Determining the scaling relationship: h2(N) ~ N^v, fitting log-log plot
    v, log_intercept = np.polyfit(np.log(N_values), np.log(h2_values), 1)
    print(f'Scaling exponent, v: {v}')

if __name__ == "__main__":
    main()
