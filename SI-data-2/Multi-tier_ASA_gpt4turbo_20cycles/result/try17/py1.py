import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def generate_unit_vector():
    """ Generates a random 3D unit vector with uniform distribution across the sphere. """
    phi = np.random.uniform(0, 2 * np.pi)
    cos_theta = np.random.uniform(-1, 1)
    sin_theta = np.sqrt(1 - cos_theta**2)
    return np.array([sin_theta * np.cos(phi), sin_theta * np.sin(phi), cos_theta])

def generate_polymer(N):
    """ Generates a polymer chain with N segments, returning end-to-end vector. """
    positions = [np.zeros(3)]
    for _ in range(N):
        positions.append(positions[-1] + generate_unit_vector())
    return np.array(positions)

def plot_polymers(Ns, num_samples=50):
    """ Plots sample polymer chains for each N in Ns. """
    for N in Ns:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for _ in range(num_samples):
            positions = generate_polymer(N)
            ax.plot(positions[:,0], positions[:,1], positions[:,2])
        plt.title(f'Polymer Chains for N={N}')
        plt.savefig(f'Chain3D{N}.png')
        plt.close()

def calculate_h2(Ns, num_chains=2000):
    """ Calculate and plot mean squared end-to-end distances for various values of N. """
    h2s = []
    for N in Ns:
        distances = [np.sum((generate_polymer(N)[-1] - np.zeros(3))**2) for _ in range(num_chains)]
        h2s.append(np.mean(distances))
        
    plt.figure()
    plt.plot(Ns, h2s, marker='o', linestyle='-')
    plt.xlabel('N (Number of Segments)')
    plt.ylabel('Mean Squared End-to-End Distance h2(N)')
    plt.savefig('h2vsN.png')
    plt.close()
    
    return h2s, Ns

def scaling_relation(h2s, Ns):
    """ Fits and prints the exponent v in the scaling law h2(N) ~ N^v. """
    coeffs = np.polyfit(np.log(Ns), np.log(h2s), 1)
    return coeffs[0]

# Parameters and execution
Ns = [10, 50, 100, 200, 400]
plot_polymers(Ns)
h2s, Ns = calculate_h2(Ns)
v = scaling_relation(h2s, Ns)
print(f"The scaling exponent v is approximately: {v:.3f}")
