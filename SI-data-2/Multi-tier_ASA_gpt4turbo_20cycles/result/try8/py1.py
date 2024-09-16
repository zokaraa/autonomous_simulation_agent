import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random

def generate_random_unit_vector():
    phi = np.random.uniform(0, np.pi * 2)
    costheta = np.random.uniform(-1, 1)
    sintheta = np.sqrt(1 - costheta**2)
    x = sintheta * np.cos(phi)
    y = sintheta * np.sin(phi)
    z = costheta
    return np.array([x, y, z])

def generate_chain(N):
    segments = [generate_random_unit_vector() for _ in range(N)]
    positions = np.cumsum(segments, axis=0)
    return positions

def calculate_h2(positions):
    return np.sum((positions[-1] - positions[0]) ** 2)

def main():
    N_values = [10, 50, 100, 200, 400]
    num_chains = 2000
    h2_values = []
    
    for N in N_values:
        chains = [generate_chain(N) for _ in range(num_chains)]
        h2 = np.mean([calculate_h2(chain) for chain in chains])
        h2_values.append(h2)
        
        # Randomly select 50 chains to visualize
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        selected_chains = random.sample(chains, 50)
        for chain in selected_chains:
            ax.plot(chain[:,0], chain[:,1], chain[:,2])
        plt.title(f"3D Random Walks with N = {N}")
        plt.savefig(f"Chain3D{N}.png")
        plt.close(fig)
    
    # Plot h2 vs N
    plt.figure()
    plt.plot(N_values, h2_values, marker='o')
    plt.xlabel('Segment count N')
    plt.ylabel('Mean squared end-to-end distance h2(N)')
    plt.title('h2(N) vs N')
    plt.savefig('h2vsNGraph.png')
    plt.close()

    # Calculate the scaling relationship
    log_N = np.log(N_values)
    log_h2 = np.log(h2_values)
    slope, intercept = np.polyfit(log_N, log_h2, 1)
    print(f"Scaling exponent v: {slope}")
    
if __name__ == "__main__":
    main()
