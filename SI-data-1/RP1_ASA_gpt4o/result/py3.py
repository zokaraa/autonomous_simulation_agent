import docx
import numpy as np
import matplotlib.pyplot as plt

def read_docx(file_path):
    """Reads content from a docx file."""
    doc = docx.Document(file_path)
    content = []
    for paragraph in doc.paragraphs:
        content.append(paragraph.text)
    return "\n".join(content)

def verify_scaling_exponent(N_values, h2_values):
    """Calculates and returns the scaling exponent v."""
    N_log = np.log(N_values)
    h2_log = np.log(h2_values)
    v, intercept = np.polyfit(N_log, h2_log, 1)
    return v

def plot_h2_vs_N(N_values, h2_values, filename):
    """Plots h2(N) vs N and saves the plot as an image file."""
    plt.figure()
    plt.plot(N_values, h2_values, 'o-', label='h2(N) measured')
    plt.xlabel('N')
    plt.ylabel('h2(N)')
    plt.title('h2(N) vs N')
    plt.legend()
    plt.savefig(filename)
    plt.show()

# Display the contents of the Word document 'Polymer_Chain_Simulation_Report.docx'
report_content = read_docx('Polymer_Chain_Simulation_Report.docx')
print("Contents of Polymer_Chain_Simulation_Report.docx:\n")
print(report_content)

# Manually input values of h2(N) and N values
N_values = [10, 50, 100, 200, 400]
h2_values = [
    10.068590515289623,
    50.47424460668347,
    99.00621447696592,
    198.29684999082588,
    400.93393546977967
]

# Calculate the scaling relationship and verify the scaling exponent
v = verify_scaling_exponent(N_values, h2_values)
print(f"\nVerified Scaling Exponent v: {v}")

# Plot h2(N) vs N for visual verification
plot_h2_vs_N(N_values, h2_values, "h2vsN_verified.png")
