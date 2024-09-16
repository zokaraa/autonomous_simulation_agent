import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def generate_random_unit_vector():
    phi = np.random.uniform(0, 2*np.pi)
    cos_theta = np.random.uniform(-1, 1)
    sin_theta = np.sqrt(1 - cos_theta**2)
    return np.array([sin_theta * np.cos(phi), sin_theta * np.sin(phi), cos_theta])

def generate_polymer_chain(N):
    chain = np.zeros((N, 3))
    for i in range(1, N):
        chain[i] = chain[i-1] + generate_random_unit_vector()
    return chain

def mean_squared_end_to_end_distance(chain):
    return np.sum((chain[-1] - chain[0])**2)

def plot_polymer_chains(chains, N):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for chain in chains:
        ax.plot(chain[:, 0], chain[:, 1], chain[:, 2])
    plt.title(f"Random Polymer Chains with N={N}")
    plt.savefig(f'Chain3D{N}.png')
    plt.close()

def calculate_and_plot_h2_vs_N(N_values):
    h2 = []
    for N in N_values:
        chains = [generate_polymer_chain(N) for _ in range(2000)]
        h2.append(np.mean([mean_squared_end_to_end_distance(chain) for chain in chains]))
        selected_chains = np.random.choice(chains, 50, replace=False)
        plot_polymer_chains(selected_chains, N)
    plt.figure()
    plt.plot(N_values, h2, 'o-')
    plt.xlabel('Number of Segments (N)')
    plt.ylabel('Mean Squared End-to-End Distance (h2)')
    plt.title('h2 vs N')
    plt.savefig('h2vsN.png')
    plt.close()
    return np.polyfit(np.log(N_values), np.log(h2), 1)[0]

# Usage of defined functions
N_values = [10, 50, 100, 200, 400]
v = calculate_and_plot_h2_vs_N(N_values)
print(f"The scaling exponent v is approximately {v:.2f}.")
