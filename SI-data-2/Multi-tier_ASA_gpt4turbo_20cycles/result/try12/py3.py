import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def generate_unit_vector():
    phi = np.random.uniform(0, 2 * np.pi)
    costheta = np.random.uniform(-1, 1)
    theta = np.arccos(costheta)  # Use numpy's arccos function to compute the angle
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    return np.array([x, y, z])

def polymer_chain(N):
    positions = np.zeros((N, 3))
    for i in range(1, N):
        positions[i] = positions[i-1] + generate_unit_vector()
    return positions

def plot_polymer_chains(N):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for _ in range(50):
        chain = polymer_chain(N)
        ax.plot(chain[:, 0], chain[:, 1], chain[:, 2])
    plt.title(f'3D Random Walk Polymer of N={N}')
    plt.savefig(f'Chain3D{N}.png')
    plt.close()
    
def mean_squared_end_to_end_distance(N, num_chains=2000):
    distances = []
    for _ in range(num_chains):
        chain = polymer_chain(N)
        distance = np.linalg.norm(chain[-1] - chain[0])
        distances.append(distance**2)
    return np.mean(distances)

N_values = [10, 50, 100, 200, 400]
means = []

# Generate and plot chains for each N value
for N in N_values:
    plot_polymer_chains(N)
    mean_h2 = mean_squared_end_to_end_distance(N)
    means.append(mean_h2)

# Plot mean squared end-to-end distance versus N
plt.plot(N_values, means, '-o')
plt.xlabel('N (Number of Segments)')
plt.ylabel('Mean Squared End-to-End Distance h2(N)')
plt.title('h2(N) vs N')
plt.grid(True)
plt.savefig('h2vsN.png')
plt.close()

# Determine the scaling relationship fitting
coefficients = np.polyfit(np.log(N_values), np.log(means), 1)
v = coefficients[0]
print(f'The estimated scaling exponent v is approximately {v:.2f}')
