import numpy as redirect_stdout
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
import numpy as np

def create_unit_vector():
    phi = np.random.uniform(0, 2*np.pi)
    costheta = np.random.uniform(-1, 1)
    theta = np.acos(costheta)
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    return np.array([x, y, z])

def polymer_chain(N):
    positions = [np.zeros(3)]
    for _ in range(1, N):
        positions.append(positions[-1] + create_unit_vector())
    return np.array(positions)

def mean_squared_end_to_end_distance(chains):
    distances = [np.linalg.norm(chain[-1] - chain[0])**2 for chain in chains]
    return np.mean(distances)

N_values = [10, 50, 100, 200, 400]
all_h2 = []

for N in N_values:
    chains = [polymer_chain(N) for _ in range(2000)]
    h2 = mean_squared_end_to_end_distance(chains)
    all_h2.append(h2)
    
    # Select 50 random chains to plot
    selected_chains = random.sample(chains, 50)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for chain in selected_chains:
        ax.plot(chain[:,0], chain[:,1], chain[:,2])
    plt.title(f'3D Polymer Chains N={N}')
    plt.savefig(f'Chain3D{N}.png')
    plt.close(fig)

# Ploting h2 vs N
plt.figure()
plt.plot(N_values, all_h2, marker='o')
plt.xscale('log')
plt.yscale('log')
plt.title('Mean Squared End-to-End Distance vs. N')
plt.xlabel('N (Number of Segments)')
plt.ylabel('Mean Squared End-to-End Distance, h2(N)')
plt.grid(True)
plt.savefig('h2vsN.png')
plt.close()

# Estimation of the scaling exponent v
log_n = np.log(N_values)
log_h2 = np.log(all_h2)
v, const = np.polyfit(log_n, log_h2, 1)
print(f'The scaling exponent v is approximately {v:.2f}')
