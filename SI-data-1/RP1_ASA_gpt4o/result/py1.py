import numpy as np
import matplotlib.pyplot as plt

def generate_unit_vector():
    """Generate a random 3D unit vector with uniform distribution on a sphere."""
    phi = np.random.uniform(0, 2 * np.pi)
    theta = np.arccos(np.random.uniform(-1, 1))  # Correctly distributed over a sphere
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    return np.array([x, y, z])

def generate_polymer_chain(N):
    """Generate a polymer chain consisting of N segments with length 1."""
    positions = [np.zeros(3)]
    for _ in range(N):
        direction = generate_unit_vector()
        new_position = positions[-1] + direction
        positions.append(new_position)
    return np.array(positions)

def compute_end_to_end_distance(chain):
    """Compute the end-to-end distance vector for a given polymer chain."""
    return np.linalg.norm(chain[-1] - chain[0])

N_values = [10, 50, 100, 200, 400]
num_chains = 2000
h2_values = []

for N in N_values:
    end_to_end_distances = []
    for _ in range(num_chains):
        chain = generate_polymer_chain(N)
        end_to_end_distance = compute_end_to_end_distance(chain)
        end_to_end_distances.append(end_to_end_distance**2)
    h2_N = np.mean(end_to_end_distances)
    h2_values.append(h2_N)
    print(f"h2({N}) = {h2_N}")

# Plotting chain conformations for each N value and saving them
for N in N_values:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for _ in range(50):
        chain = generate_polymer_chain(N)
        ax.plot(chain[:,0], chain[:,1], chain[:,2])
    plt.title(f"Chain Conformations for N = {N}")
    plt.savefig(f"Chain3D{N}.png")
    plt.close()

# Plotting h2(N) vs N
plt.figure()
plt.plot(N_values, h2_values, 'o-')
plt.xlabel('N')
plt.ylabel('h2(N)')
plt.title('h2(N) vs. N')
plt.savefig("h2vsN.png")
plt.close()

# Determining the scaling relationship h2(N) ∝ N^v
N_log = np.log(N_values)
h2_log = np.log(h2_values)
v, _ = np.polyfit(N_log, h2_log, 1)
print(f"Scaling exponent v: {v}")
