import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def generate_unit_vector():
    # Generating a random unit vector in 3D
    phi = np.random.uniform(0, 2 * np.pi)
    costheta = np.random.uniform(-1, 1)
    sintheta = np.sqrt(1 - costheta**2)
    return np.array([sintheta * np.cos(phi), sintheta * np.sin(phi), costheta])

def generate_polymer_chain(N):
    polymer = [np.zeros(3)]
    for _ in range(1, N):
        next_segment = generate_unit_vector()
        polymer.append(polymer[-1] + next_segment)
    return np.array(polymer)

def calculate_mean_squared_distance(p):
    return np.sum((p[-1] - p[0])**2)

def plot_chains(N, sample_size):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for _ in range(sample_width):  # 'sample_width' should be 'sample_size'
        chain = generate_polymer_chain(N)
        ax.plot(chain[:,0], chain[:,1], chain[:,2])
    plt.title(f'3D Conformations for N={N}')
    plt.savefig(f'Chain3D{N}.png')
    plt.close()

# Parameters setup
Ns = [10, 50, 100, 200, 400]
num_chains = 2000
sample_width = 50  # 'sample_width' should be renamed consistently
mean_squared_distances = []

for N in Ns:
    distances = []
    for _ in range(num_chains):
        polymer = generate_polymer_chain(N)
        distances.append(calculate_mean_squared_distance(polymer))
    mean_squared_distance = np.mean(distances)
    mean_squared_distances.append(mean_squared_distance)
    plot_chains(N, sample_width)  # 'sample_width' should be passed as 'sample_size'

# Plot mean squared distance vs. N
plt.figure()
plt.plot(Ns, mean_squared_distances, marker='o')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('N (Number of Segments)')
plt.ylabel('Mean Squared End-to-End Distance, h2(N)')
plt.title('h2(N) Scaling with Chain Length N')
plt.savefig('h2vsN.png')
plt.close()

# Calculate scaling exponent v from log-log plot
log_Ns = np.log(Ns)
log_mean_squared_distances = np.log(mean_squared_distances)  # Corrected variable name
v, _ = np.polyfit(log_Ns, log_mean_squared_distances, 1)

print(f"The scaling exponent v is: {v}")
