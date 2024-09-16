import numpy as np
import matplotlib.pyplot as plt

def generate_random_direction():
    """Generate a random unit vector uniformly distributed in 3D space."""
    phi = np.random.uniform(0, 2 * np.pi)
    cos_theta = np.random.uniform(-1, 1)
    sin_theta = np.sqrt(1 - cos_theta ** 2)
    x = sin_theta * np.cos(phi)
    y = sin_theta * np.sin(phi)
    z = cos_theta
    return np.array([x, y, z])

def generate_polymer_chain(N):
    """Generate a polymer chain with N segments."""
    chain = [np.array([0.0, 0.0, 0.0])]
    for _ in range(N):
        direction = generate_random_direction()
        new_segment = chain[-1] + direction
        chain.append(new_segment)
    return np.array(chain)

def compute_end_to_end_distance(chain):
    """Compute the end-to-end distance vector of a polymer chain."""
    return np.linalg.norm(chain[-1] - chain[0])

def polymer_simulation(N, num_chains=2000):
    chains = [generate_polymer_chain(N) for _ in range(num_chains)]
    end_to_end_distances = [compute_end_to_end_distance(chain) for chain in chains]
    mean_squared_distance = np.mean(np.array(end_to_end_distances) ** 2)
    return chains, mean_squared_distance

def plot_chains(chains, N):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for chain in np.random.choice(chains, 50, replace=False):
        ax.plot(chain[:, 0], chain[:, 1], chain[:, 2])
    plt.title(f'Polymer Chains (N={N})')
    plt.savefig(f'Chain3D{N}.png')
    plt.close()

def plot_h2_vs_N(h2_values, N_values):
    plt.figure()
    plt.plot(N_values, h2_values, marker='o')
    plt.xlabel('N (Number of Segments)')
    plt.ylabel('$h^2(N)$ (Mean Squared End-to-End Distance)')
    plt.title('$h^2(N)$ vs. N')
    plt.savefig('h2vsN.png')
    plt.close()

def main():
    N_values = [10, 50, 100, 200]
    h2_values = []

    for N in N_values:
        chains, h2_N = polymer_simulation(N)
        h2_values.append(h2_N)
        plot_chains(chains, N)
        print(f'Mean squared end-to-end distance for N={N}: {h2_N}')
    
    # Determine scaling relationship h^2(N) ∝ N^v
    coeffs = np.polyfit(np.log(N_values), np.log(h2_values), 1)
    v = coeffs[0]
    print(f'Scaling exponent v: {v}')
    
    plot_h2_vs_N(h2_values, N_values)

if __name__ == "__main__":
    main()
