import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

def generate_unit_vector():
    phi = np.random.uniform(0, np.pi*2)
    costheta = np.random.uniform(-1, 1)
    u = np.random.uniform(0, 1)
    theta = np.acos(costheta)
    r = u**(1/3)
    sintheta = np.sin(theta)
    x = r * np.cos(phi) * sintheta
    y = r * np.sin(phi) * sintheta
    z = r * costheta
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
    h2_values = [mean_squared_distances[N] for N in Ns]
    plt.plot(Ns, h2_values, marker='o', linestyle='-')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('N (Number of segments)')
    plt.ylabel('Mean Squared End-to-End Distance h2(N)')
    plt.title('h2 vs N on a log-log scale')
    plt.savefig('./plots/h2vsN.png')
    plt.close()

    # Determine scaling relationship
    coefficients = np.polyfit(np.log(Ns), np.log(h2_values), 1)
    scaling_exponent = coefficients[0]
    print(f'The scaling relationship exponent v is approximately {scaling_exponent}')

if __name__ == "__main__":
    main()

