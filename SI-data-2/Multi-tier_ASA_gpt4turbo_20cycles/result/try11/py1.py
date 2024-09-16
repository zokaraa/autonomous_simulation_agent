import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def random_unit_vector():
    phi = np.random.uniform(0, 2*np.pi)
    costheta = np.random.uniform(-1, 1)
    theta = np.acos(costheta)
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    return np.array([x, y, z])

def generate_polymer(N):
    positions = np.zeros((N, 3))
    for i in range(1, N):
        positions[i] = positions[i - 1] + random_unit_vector()
    return positions

def compute_h2(polymer_positions):
    return np.sum((polymer_positions[-1] - polymer_positions[0])**2)

Ns = [10, 50, 100, 200, 400]
mean_h2 = []
for N in Ns:
    h2s = []
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    for _ in range(50):
        polymer = generate_polymer(N)
        ax.plot(polymer[:, 0], polymer[:, 1], polymer[:, 2], alpha=0.4)
        
        if _ < 2000:  # Collect 2000 polymer samples for statistical purposes.
            h2s.append(compute_h2(polymer))
    
    mean_h2.append(np.mean(h2s))
    plt.title(f'3D Polymer Chains with N={N}')
    plt.savefig(f'Chain3D{N}.png')
    plt.close()

plt.figure()
plt.plot(Ns, mean_h2, 'o-')
plt.xlabel('Number of Segments (N)')
plt.ylabel('Mean Squared End-to-End Distance (h2)')
plt.title('Mean Squared Distance vs. Chain Length')
plt.savefig('h2vsN.png')
plt.close()

v, _ = np.polyfit(np.log(Ns), np.log(mean_h2), 1)
print(f"The scaling exponent v is approximately {v:.2f}")
