import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def generate_random_unit_vector():
    phi = np.random.uniform(0, 2 * np.pi)
    costheta = np.random.uniform(-1, 1)
    sintheta = np.sqrt(1 - costheta**2)
    x = sintheta * np.cos(phi)
    y = sintheta * np.sin(phi)
    z = costheta
    return np.array([x, y, z])

def generate_polymer_chain(N):
    positions = np.zeros((N + 1, 3))
    for i in range(1, N + 1):
        positions[i] = positions[i - 1] + generate_random_unit_vector()
    return positions

def calculate_h2(polymer_chains):
    h2 = np.mean([np.sum((chain[-1] - chain[0])**2) for chain in polymer_chains])
    return h2

def main():
    N_values = [10, 50, 100, 200, 400]
    h2_values = []
    num_chains = 2000
    
    for N in N_values:
        chains = [generate_polymer_chain(N) for _ in range(num_chains)]
        h2 = calculate_h2(chains)
        h2_values.append(h2)
        
        # Select 50 random chains and plot them
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        indices = np.random.choice(len(chains), 50, replace=False)
        for index in indices:
            ax.plot(chains[index][:, 0], chains[index][:, 1], chains[index][:, 2])
        plt.title(f'Random 50 Polymer Chains for N = {N}')
        plt.savefig(f'Chain3D{N}.png')
        plt.close()

    # Plot h2(N) vs N
    plt.figure(figsize=(8, 6))
    plt.plot(N_values, h2_values, marker='o', linestyle='-', color='b')
    plt.xlabel('Number of segments (N)')
    plt.ylabel('Mean squared end-to-end distance (h2)')
    plt.title('h2 vs N')
    plt.savefig('h2vsN.png')
    plt.close()

    # Compute the scaling relationship
    coeffs = np.polyfit(np.log(N_values), np.log(h2_values), 1)
    v = coeffs[0]
    print(f'The scaling exponent v is approximately: {v}')

if __name__ == "__main__":
    main()
