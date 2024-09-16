import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def generate_unit_vector():
    phi = np.random.uniform(0, np.pi * 2)
    costheta = np.random.uniform(-1, 1)
    theta = np.arccos(costheta)
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    return np.array([x, y, z])

def generate_polymer_chain(n):
    return np.cumsum([generate_unit_vector() for _ in range(n)], axis=0)

def calculate_end_to_end_distance(chain):
    return np.linalg.norm(chain[-1] - chain[0])

def main():
    N_values = [10, 50, 100, 200, 400]
    num_samples = 2000
    h2_values = []
    for N in N_values:
        distances = []
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for _ in range(num_samples):
            chain = generate_polymer_chain(N)
            distances.append(calculate_end_to_end_distance(chain) ** 2)
            if _ < 50:  # Only plot 50 random samples
                ax.plot(chain[:, 0], chain[:, 1], chain[:, 2], alpha=0.5)
        h2 = np.mean(distances)
        h2_values.append(h2)
        ax.set_title(f"3D Random Walks with N = {N}")
        plt.savefig(f'Chain3D{N}.png')
        plt.close()

    # Plotting h2(N) vs N
    plt.figure()
    plt.loglog(N_values, h2_values, marker='o')
    plt.xlabel("N")
    plt.ylabel("Mean Squared End-to-End Distance [h2(N)]")
    plt.title("h2(N) vs N on Log-Log Scale")
    plt.savefig('h2vsN.png')
    plt.close()

    # Fitting to check scaling relation h2(N) ~ N^v
    coeffs = np.polyfit(np.log(N_values), np.log(h2_values), 1)
    v = coeffs[0]
    print(f"Scaling exponent v is approximately: {v:.2f}")

if __name__ == "__main__":
    main()
