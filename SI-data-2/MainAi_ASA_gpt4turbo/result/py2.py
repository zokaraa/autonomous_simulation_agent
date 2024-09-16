import numpy as np

def generate_random_unit_vector():
    """Generates a random 3D unit vector."""
    phi = np.random.uniform(0, np.pi * 2)
    costheta = np.random.uniform(-1, 1)
    theta = np.arccos(costheta)
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    return np.array([x, y, z])

def generate_polymer_chain(N):
    """Generates one polymer chain of N segments."""
    chain = [np.array([0, 0, 0])]  # Start at origin
    for _ in range(1, N):
        orientation = generate_random_unit_vector()
        chain.append(chain[-1] + orientation)
    return np.array(chain)

def compute_h2(N, num_chains=2000):
    """Computes mean squared end-to-end distance for polymer chains."""
    h2_values = []
    for _ in range(num_chains):
        chain = generate_polymer_chain(N)
        end_to_end_vector = chain[-1] - chain[0]
        h2_values.append(np.linalg.norm(end_to_end_vector)**2)
    return np.mean(h2_values)

# Set segment numbers for generating data
Ns = [10, 50, 100, 200, 400]
h2_results = {}

# Generate polymer chains and compute h2 for each N
for N in Ns:
    h2_results[N] = compute_h2(N)

# Print results
print("h2 results:", h2_results)
