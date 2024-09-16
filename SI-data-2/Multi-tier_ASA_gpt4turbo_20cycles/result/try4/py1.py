import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def generate_vector():
    phi = np.random.uniform(0, np.pi * 2)
    costheta = np.random.uniform(-1, 1)
    theta = np.arccos(costheta)
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    return np.array([x, y, z])

def generate_polymer_chain(N):
    chain = np.zeros((N, 3))
    for i in range(1, N):
        chain[i] = chain[i-1] + generate_vector()
    return chain

def calculate_end_to_end(chain):
    return np.linalg.norm(chain[-1] - chain[0])

def plot_polymer_chains(N, chains):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for chain in chains:
        ax.plot(chain[:, 0], chain[:, 1], chain[:, 2])
    plt.title(f'3D Random Walks with N = {N}')
    plt.savefig(f'Chain3D{N}.png')
    plt.close()

def main():
    N_values = [10, 50, 100, 200, 400]
    h2_values = []

    for N in N_values:
        distances_squared = []
        selected_chains = []
        for _ in range(2000):
            chain = generate_polymer_chain(N)
            if len(selected_chains) < 50:
                selected_chains.append(chain)
            distance = calculate_end_to_end(chain)
            distances_squared.append(distance ** 2)
        
        h2 = np.mean(distances_squared)
        h2_values.append(h2)
        
        plot_polymer_chains(N, selected_chains)

    plt.figure()
    plt.plot(N_values, h2_values, 'o-')
    plt.title('Mean Squared End-to-End Distance vs. N')
    plt.xlabel('N (Number of Segments)')
    plt.ylabel('Mean Squared Distance')
    plt.savefig('h2vsN.png')

    # Fit to find scaling relation h2(N) = c * N^v
    coeffs = np.polyfit(np.log(N_values), np.log(h2_values), 1)
    v = coeffs[0]
    print(f"Scaling exponent v: {v}")

if __name__ == "__main__":
    main()
