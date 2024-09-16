import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random

# Assume 'generate_random_unit_vector' and 'generate_polymer_chain' methods are defined elsewhere
def generate_random_unit_vector():
    """ Generate a random unit vector in 3D space """
    phi = random.uniform(0, 2 * np.pi)
    costheta = random.uniform(-1, 1)
    sintheta = np.sqrt(1 - costheta * costheta)
    x = sintheta * np.cos(phi)
    y = sintheta * np.sin(phi)
    z = costheta
    return np.array([x, y, z])

def generate_polymer_chain(N):
    """ Generate a polymer chain of N segments """
    positions = [np.array([0, 0, 0])]  # Start at the origin
    for _ in range(1, N):
        new_segment = generate_random_unit_vector()
        positions.append(positions[-1] + new_segment)
    return np.array(positions)

def plot_polymer_chains(N, num_samples=50):
    """Plots random polymer chain conformations."""
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    for _ in range(num_samples):
        chain = generate_polymer_chain(N)
        ax.plot(chain[:, 0], chain[:, 1], chain[:, 2])
    
    plt.title(f"3D Conformations of {N}-segment Polymer Chains")
    plt.savefig(f"Chain3D{N}.png")
    plt.close()

def plot_h2_vs_N(h2_results):
    """Plots mean squared end-to-end distance vs. number of segments."""
    Ns = list(h2_results.keys())
    h2_values = list(h2_results.values())
    
    plt.figure(figsize=(8, 6))
    plt.plot(Ns, h2_values, marker='o')
    
    plt.xlabel("Number of Segments (N)")
    plt.ylabel("Mean Squared End-to-End Distance (h2)")
    plt.title("h2 vs. N")
    plt.savefig("h2vsN.png")
    plt.close()

def determine_scaling_relationship(h2_results):
    """Determines the scaling relationship h2(N) ~ N^v and prints v."""
    Ns = np.array(list(h2_results.keys()))
    h2_values = np.array(list(h2_results.values()))
    
    log_Ns = np.log(Ns)
    log_h2 = np.log(h2_values)
    
    slope, intercept = np.polyfit(log_Ns, log_h2, 1)
    print(f"Scaling relationship: h2(N) ~ N^{slope:.4f}")

# Use previously computed h2 results
h2_results = {10: 8.93138321455007, 50: 49.19968196570601, 100: 99.01376484962115, 200: 204.2821190730705, 400: 390.79555639807637}

# Plot chain conformations and mean squared end-to-end distances
for N in h2_results.keys():
    plot_polymer_chains(N)

plot_h2_vs_N(h2_results)
determine_scaling_relationship(h2_results)
