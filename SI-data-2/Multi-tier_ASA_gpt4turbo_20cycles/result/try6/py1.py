import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
np.random.seed(42)

def generate_chain(N):
    angles_theta = np.arccos(2 * np.random.rand(N) - 1)
    angles_phi = 2 * np.pi * np.random.rand(N)
    x = np.sin(angles_theta) * np.cos(angles_phi)
    y = np.sin(angles_theta) * np.sin(angles_phi)
    z = np.cos(angles_theta)
    vectors = np.column_stack((x, y, z))
    return np.cumsum(vectors, axis=0)

def plot_chains(N, num_chains=50):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for _ in range(num_chains):
        chain = generate_chain(N)
        ax.plot(chain[:, 0], chain[:, 1], chain[:, 2])
    plt.title(f'3D Random Walks for N={N}')
    plt.savefig(f'Chain3D{N}.png')
    plt.close()

def calculate_h2(N_samples=2000):
    N_list = [10, 50, 100, 200, 400]
    h2_vals = []
    for N in N_list:
        h2_sum = 0
        for _ in range(N_samples):
            chain = generate_chain(N)
            h2_sum += np.sum((chain[-1] - chain[0])**2)
        h2 = h2_sum / N_samples
        h2_vals.append(h2)
        plot_chains(N)
    plt.plot(N_list, h2_vals, 'o-', label="h2(N) vs. N")
    plt.xlabel('N')
    plt.ylabel('h2(N)')
    plt.title('Mean Squared End-to-End Distance vs. N')
    plt.savefig('h2vsN.png')
    plt.close()
    return N_list, h2_void

def estimate_v(N_list, h2_vals):
    coeffs = np.polyfit(np.log(N_list), np.log(h2_vals), 1)
    return coeffs[0]

def main():
    N_list, h2_vals = calculate_h2()
    v = estimate_v(N_list, h2_vals)
    print(f"Estimated scaling exponent v: {v}")

if __m.__name__ == "__main__":
    main()
