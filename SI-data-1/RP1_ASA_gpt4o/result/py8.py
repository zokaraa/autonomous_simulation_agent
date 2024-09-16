import os
import hashlib
from os import path

def create_html_report(N_values, h2_values, scaling_exponent, checksums, output_dir):
    """Create an HTML report summarizing the simulation results."""
    # Create the HTML Content
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Polymer Chain Simulation Experiment Report</title>
    </head>
    <body>
        <h1>Polymer Chain Simulation Experiment Report</h1>
        
        <h2>Abstract</h2>
        <p>
        This report provides an analysis of a simulation study on polymer chains. 
        The primary objective was to generate 2000 polymer chains consisting of N segments with random orientations in 3D space, 
        calculate the mean squared end-to-end distance (h2(N)), and determine the relationship of h2(N) with N. 
        Understanding the behavior of polymer chains is crucial for many applications in material science and biology, 
        especially in predicting the physical properties of macromolecules. 
        A key result from this study is the determination of the scaling exponent 'v' that characterizes the relationship between 
        the mean squared end-to-end distance and the number of segments.
        </p>
        
        <h2>Introduction</h2>
        <p>
        The study of polymer chains is significant in understanding the physical properties 
        of macromolecules in materials science and biology. Polymers are large molecules made up of repeating subunits called monomers, 
        and their structure affects their function and behavior in various environments. 
        A polymer chain can be modeled as a series of connected segments, with each segment having a fixed length but random orientation. 
        This random orientation gives rise to the study of random walks and their properties. 
        The objective of this study was to simulate 2000 polymer chains for various lengths (N) ranging from 10 to 400 segments and analyze 
        the mean squared end-to-end distance (h2(N)) as a function of N.
        </p>
        <p>
        The end-to-end distance of a polymer chain is a measure of the spatial extent of the polymer, 
        which impacts its physical properties such as viscosity, tensile strength, and diffusion. 
        The theoretical background suggests that the mean squared end-to-end distance should scale with the number of segments as h2(N) ∝ N^v, 
        where the exponent 'v' can indicate the type of polymer chain model, such as ideal (or Gaussian) chains, self-avoiding walks, or others. 
        This study aims to empirically determine the scaling exponent 'v' and compare it with theoretical expectations for ideal polymer chains.
        </p>
        
        <h2>Methods</h2>
        <p>
        The simulation was implemented using Python, leveraging the numpy library for numerical computations and matplotlib for data visualization. 
        For each polymer chain, 3D unit vectors representing segment orientations were generated using a uniform distribution over a sphere. 
        This method ensures that the directions of segments are uniformly distributed in three-dimensional space. 
        The polymer chains were constructed by cumulatively adding these vectors starting from the origin, thus forming a random walk in three dimensions. 
        The end-to-end distance was computed as the Euclidean distance between the first and last segment of each polymer chain. 
        This computation was repeated for 2000 chains for each given N to obtain a statistically significant result. 
        The mean squared end-to-end distance, h2(N), was calculated by averaging the squared end-to-end distances over the 2000 chains for each N value. 
        To visualize the polymer chains, 50 random chain conformations were plotted for each N value. Additionally, a graph of h2(N) versus N was plotted to study the scaling behavior. 
        Linear regression on log-transformed data was used to determine the scaling exponent 'v', providing insights into the relationship between h2(N) and N.
        </p>
        
        <h2>Results</h2>
        <p>
        The results of the simulation are summarized in the table and figures below. 
        The mean squared end-to-end distances for different N values were computed as follows:
        </p>
        <ul>
        """
    
    for i, N in enumerate(N_values):
        html_content += f"<li>h2({N}) = {h2_values[i]:.2f}</li>"
    
    html_content += f"""
        </ul>
        <p>
        These values are close to the corresponding N values, as expected for an ideal polymer chain model where h2(N) is proportional to N. 
        The scaling exponent 'v' was determined to be approximately {scaling_exponent:.4f} through linear regression on the log-transformed values of N and h2(N). 
        This value is consistent with the theoretical prediction for ideal chains, where 'v' is expected to be 1.
        </p>
        """
    
    for file in ['Chain3D10.png', 'Chain3D50.png', 'Chain3D100.png', 'Chain3D200.png', 'Chain3D400.png']:
        img_path = path.join(output_dir, file)
        if path.exists(img_path):
            html_content += f'<h3>Figure: Chain Conformations for {file[7: file.find(".png")]} segments</h3>'
            html_content += f'<img src="{file}" alt="{file}" style="width:400px;"><br>'

    if path.exists(path.join(output_dir, 'h2vsN.png')):
        html_content += '<h3>Figure: Mean squared end-to-end distance (h2(N)) vs N</h3>'
        html_content += '<img src="h2vsN.png" alt="h2vsN.png" style="width:400px;"><br>'

    html_content += """
        <h2>Files Summary</h2>
        <table border="1">
            <tr>
                <th>File</th>
                <th>Checksum</th>
            </tr>
        """
    
    for file_name, checksum in checksums.items():
        html_content += f"<tr><td>{file_name}</td><td>{checksum}</td></tr>"

    html_content += """
        </table>
    </body>
    </html>
    """
    
    with open(path.join(output_dir, 'report.html'), 'w') as file:
        file.write(html_content)

    # Print completion message
    print(f"HTML report created at: {path.join(output_dir, 'report.html')}")

# Main execution

# N values and relevant data
N_values = [10, 50, 100, 200, 400]
h2_values = [
    10.126149898135866,
    48.84597309146922,
    99.67816248963773,
    202.85695577701915,
    405.66744630809154
]
scaling_exponent = 1.002402565584748

# Directory containing results
results_dir = 'results'

# Generate file checksums
file_checksums = {}
for root, _, files in os.walk(results_dir):
    for file in files:
        file_path = path.join(root, file)
        with open(file_path, 'rb') as f:
            file_hash = hashlib.md5()
            while chunk := f.read(8192):
                file_hash.update(chunk)
            file_checksums[file] = file_hash.hexdigest()

# Create HTML report
create_html_report(N_values, h2_values, scaling_exponent, file_checksums, results_dir)
