import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
import argparse

def generate_random_unit_vector():
    theta = np.random.uniform(0, np.pi*2)
    phi = np.arccos(2 * np.random.uniform(0, 1) - 1)
    x = np.sin(phi) * np.cos(theta)
    y = np.sin(phi) * np.sin(theta)
    z = np.cos(phi)
    return np.array([x, y, z])

def generate_polymer_chain(N):
    positions = np.zeros((N, 3))
    for i in range(1, N):
        positions[i] = positions[i - 1] + generate_random_unit_vector()
    return positions

def calculate_end_to_end_distance(chain):
    return np.sum((chain[-1] - chain[0])**2)

def plot_polymer_chains(N, chains_to_plot):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    for chain in chains_to_plot:
        ax.plot(chain[:, 0], chain[:, 1], chain[:, 2])
    plt.title(f'Polymer Chains with N={N}')
    plt.savefig(f'Chain3D_{N}.png')
    plt.close()

def main(N):
    num_chains = 2000
    end_to_end_distances = []
    sample_chains = random.sample(range(num_chains), 50)
    chains_to_plot = []
    
    for i in range(num_chains):
        chain = generate_polymer_chain(N)
        distance = calculate_end_to_end_distance(chain)
        end_to_end_distances.append(distance)
        if i in sample_chains:
            chains_to_plot.append(chain)
    
    plot_polymer_chains(N, chains_to_plot)
    h2 = np.mean(end_to_end_distances)
    
    # Save end-to-end distances and N to a text file
    with open(f'results_{N}.txt', 'w') as f:
        f.write(f'N={N}\n')
        f.write(f'Mean Square End-to-End Distance h2(N)={h2}\n')
        for distance in end_to_end_distances:
            f.write(f'{distance}\n')
    
    print(f'N={N}, Mean Square End-to-End Distance h2(N)={h2}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculate mean square end-to-end distance for polymer chains')
    parser.add_argument('-n', type=int, required=True, help='Number of monomers in the polymer chain')
    args = parser.parse_args()
    main(args.n)
