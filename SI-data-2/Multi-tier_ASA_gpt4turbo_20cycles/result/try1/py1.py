import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# <<<subtask: Generate 2000 polymer chains with random 3D orientations>>>
# <<<subtask: Compute the mean squared end-to-end distance for chain lengths of N=10, 50, 100, 200, 400>>>
# <<<subtask: Plot and save the graphs of 50 random chain conformations for each specified N>>>
# <<<subtask: Plot and save the mean squared end-to-end distance vs N>>>
# <<<subtask: Determine the scaling relationship h2(N) proportional to N^v and print the estimated v>>>

def generate_unit_vector():
    phi = np.random.uniform(0, np.pi*2)
    costheta = np.random.uniform(-1, 1)
    theta = np.arccos(costheta)
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    return np.array([x, y, z])

def generate_polymer_chain(N):
    return np.cumsum([generate_unit_vector() for _ in range(N)], axis=0)

def compute_h2(chains):
    return np.mean(np.sum((chains[:, -1] - chains[:, 0]) ** 2, axis=1))

N_values = [10, 50, 100, 200, 400]
h2_values = []
num_chains = 2000
show_cases = 50

for N in N_values:
    chains = np.array([generate_polymer_chain(N) for _ in range(num_chains)])
    h2_values.append(compute_h2(chains))
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'3D Conformations for N={N}')
    
    # Plot random 50 chains
    random_indices = np.random.choice(num_chains, show_cases, replace=False)
    for idx in random_indices:
        ax.plot(chains[idx,:,0], chains[idx,:,1], chains[idx,:,2])
    
    plt.savefig(f'Chain3D{N}.png')
    plt.close()

# Plot h2 vs N
plt.figure()
plt.plot(N_values, h2_values, 'bo-')
plt.xlabel('N (number of segments)')
plt.ylabel('mean squared end-to-end distance h2(N)')
plt.title('Mean Squared End-to-End Distance vs N')
plt.savefig('h2vsN.png')
plt.close()

# Estimate scaling relationship
coeffs = np.polyfit(np.log(N_values), np.log(h2_values), 1)
v = coeffs[0]
print('Scaling constant v:', v)

# End of subtasks >>>
