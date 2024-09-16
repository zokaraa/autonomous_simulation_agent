import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

def generate_unit_vector():
    phi = np.random.uniform(0, 2*np.pi)
    costheta = np.random.uniform(-1, 1)
    theta = np.arccos(costheta)
    sintheta = np.sin(theta)
    x = np.cos(phi) * sintheta
    y = np.sin(phi) * sintheta
    z = costheta
    return np.array([x, y, z])

def generate_chain(N):
    chain = np.zeros((N, 3))
    for i in range(1, N):
        chain[i] = chain[i-1] + generate_unit_vector()
    return chain

def compute_h2(chains):
    return np.mean([np.sum((chain[-1] - chain[0])**2) for chain in chains])

def plot_chains(chains, N):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    for chain in chains:
        ax.plot(chain[:, 0], chain[:, 1], chain[:, 2])
    plt.title(f'Polymer Chain Conformations for N={N}')
    plt.savefig(f'Chain3D{N}.png')
    plt.close()

def main():
    N_values = [10, 50, 100, 200, 400]
    mean_squared_distances = {}
    os.makedirs('./plots', exist_ok=True)

    for N in N_values:
        all_chains = [generate_chain(N) for _ in range(2000)]
        selected_chains = np.random.choice(all_chains, 50, replace=False)
        plot_chains(selected_chains, N)
        h2 = compute_h2(all_chains)
        mean_squared_distances[N] = h2
        print(f'For N={N}, mean squared end-to-end distance h2(N) = {h2}')
    
    # Plot h2 vs N
    plt.figure()
    Ns = list(mean_squared_distances.keys())
    h2_values = list(mean_squared_dist...[++188 chars]
