import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def random_unit_vector():
    phi = np.random.uniform(0, 2*np.pi)
    costheta = np.random.uniform(-1, 1)
    sintheta = np.sqrt(1 - costheta**2)
    x = sintheta * np.cos(phi)
    y = sintheta * np.sin(phi)
    z = costheta
    return np.array([x, y, z])

def generate_chain(N):
    segments = [random_unit_vector() for _ in range(N)]
    positions = np.cumsum(segments, axis=0)
    return positions

def calculate_h2_chains(num_chains, N):
    end_to_end_distances = []
    for _ in range(num_chains):
        chain = generate_chain(N)
        distance = np.linalg.norm(chain[-1] - chain[0])
        end_to_end_distances.append(distance**2)
    return np.mean(end_to_end_distances)

def plot_chains(N, num_samples=50):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for _ in range(num_samples):
        chain = generate_chain(N)
        ax.plot(chain[:,0], chain[:,1], chain[:,2])
    plt.savefig(f'Chain3D{N}.png')

def plot_h2_vs_N(N_values, h2_values):
    plt.figure()
    plt.plot(N_values, h2_values, marker='o')
    plt.xlabel('N (number of segments)')
    plt.ylabel('Mean squared end-to-end distance h2(N)')
    plt.title('h2(N) vs. N')
    plt.savefig('h2vsN.png')

def find_scaling_relationship(N_values, h2_values):
    coeffs = np.polyfit(np.log(N_values), np.log(h2_values), 1)
    return coeffs[0]

if __name__ == "__main__":
    N_values = [10, 50, 100, 200, 400]
    h2_values = []
    num_chains = 2000
    
    for N in N_values:
        h2 = calculate_h2_chains(num_chains, N)
        h2_values.append(h2)
        plot_chains(N)
    
    plot_h2_vs_N(N_values, h2_values)
    exponent_v = find_scaling_relationship(N_values, h2_values)
    print(f'The scaling relationship exponent v is approximately: {exponent_v:.2f}')
