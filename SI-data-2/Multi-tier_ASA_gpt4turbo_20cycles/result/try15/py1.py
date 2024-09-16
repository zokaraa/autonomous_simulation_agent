import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

def random_unit_vector():
    phi = np.random.uniform(0, np.pi*2)
    costheta = np.random.uniform(-1, 1)
    sintheta = np.sqrt(1 - costheta**2)
    x = sintheta * np.cos(phi)
    y = sintheta * np.sin(phi)
    z = costheta
    return np.array([x, y, z])

def generate_polymer_chain(N):
    segments = [random_unit_vector() for _ in range(N)]
    positions = np.cumsum(segments, axis=0)
    return positions

def plot_polymer_chains(N, num_plots=50):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for _ in range(num_plots):
        positions = generate_polymer_chain(N)
        ax.plot(positions[:, 0], positions[:, 1], positions[:, 2])
    plt.title(f'3D Conformation of {N}-Segment Polymer Chains')
    plt.savefig(f'Chain3D{N}.png')
    plt.close()

def compute_h2(N, trials=2000):
    end_to_end_distances = []
    for _ in range(trials):
        positions = generate_polymer_chain(N)
        distance_vector = positions[-1] - positions[0]
        end_to_end_distances.append(np.dot(distance_vector, distance_vector))
    return np.mean(end_to_end_distances)

def plot_h2_vs_N(N_values):
    h2_values = [compute_h2(N) for N in N_values]
    plt.plot(N_values, h2_values, marker='o')
    plt.xlabel('Number of Segments (N)')
    plt.ylabel('Mean Squared End-to-End Distance h2(N)')
    plt.title('Mean Squared End-to-End Distance vs. Number of Segments')
    plt.savefig('h2vsN.png')
    plt.close()
    return h2_values

def main():
    N_values = [10, 50, 100, 200, 400]
    for N in N_values:
        plot_polymer_chains(N)

    h2_vals = plot_h2_vs_N(N_values)
    coeffs = np.polyfit(np.log(N_values), np.log(h2_vals), 1)
    print(f"Scaling exponent v: {coeffs[0]}")

if __name__ == "__main__":
    main()
