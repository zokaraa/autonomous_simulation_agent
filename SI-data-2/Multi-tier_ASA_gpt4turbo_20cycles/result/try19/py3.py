import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def random_unit_vector():
    phi = np.random.uniform(0, 2 * np.pi)
    costheta = np.random.uniform(-1, 1)
    sintheta = np.sqrt(1 - costheta**2)
    return np.array([sintheta * np.cos(phi), sintheta * np.sin(phi), costheta])

def generate_polymer_chain(N):
    chain = [random_unit_onelector() for _ in range(N)]
    return np.cumsum(chain, axis=0)

def calculate_h2(polymers):
    return np.mean(np.sum((polymers[:, -1] - polymers[:, 0])**2, axis=1))

def plot_chains(chains, N):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    for chain in chains:
        ax.plot(chain[:, 0], chain[:, 1], chain[:, 2], alpha=0.5)
    plt.title(f'3D Random Walks for N={N}')
    plt.savefig(f'Chain3D{N}.png')
    plt.close()

def main():
    N_values = [10, 50, 100, 200, 400]
    h2_values = []
    all_chains = []

    for N in N_values:
        chains = np.array([generate_polymer_chain(N) for _ in range(2000)])
        all_chains.append(chains)
        h2 = calculate_h2(chains)
        h2_values.append(h2)
    
    for index, chains in enumerate(all_chains):
        indices = np.random.choice(len(chains), 50, replace=False)  # Corrected line
        selected_chains = chains[indices]  # Access selected chains correctly
        plot_chains(selected_chains, N_values[index])
    
    plt.figure(figsize=(8, 6))
    plt.plot(N_values, h2_values, 'o-')
    plt.xlabel('Number of Segments (N)')
    plt.ylabel('Mean Squared End-to-End Distance h2(N)')
    plt.xscale('log')
    plt.yscale('log')
    plt.title('h2(N) vs. N in Log-Log Scale')
    plt.savefig('h2vsN.png')
    plt.close()

    # Estimating the power-law exponent
    v, _ = np.polyfit(np.log(N_values), np.log(h2_values), 1)
    print(f"The scaling relationship h2(N) is proportional to N^{v:.2f}")

if __name__ == "__main__":
    main()
