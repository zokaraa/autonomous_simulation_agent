import paramiko
import os
import time
import numpy as np
import matplotlib.pyplot as plt

# Remote node information
hostname = '*****'
username = '*****'
password = '*****'
remote_path = '*****'
python_path = '*****'

def upload_file(sftp, local_path, remote_path):
    sftp.put(local_path, remote_path)

def download_file(sftp, remote_path, local_path):
    sftp.get(remote_path, local_path)

def run_remote_command(ssh, command):
    stdin, stdout, stderr = ssh.exec_command(command)
    return stdout.read().decode('utf-8'), stderr.read().decode('utf-8')

def check_file_exists(sftp, remote_path):
    try:
        sftp.stat(remote_path)
        return True
    except IOError:
        return False

def main():
    # Connect to remote node
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    sftp = ssh.open_sftp()

    # Upload py1.py to remote node
    upload_file(sftp, 'py1.py', f'{remote_path}/py1.py')

    # Run py1.py for different N values
    n_values = [100, 200, 300, 400, 600, 800]
    for n in n_values:
        command = f"bash -l -c 'cd {remote_path} && {python_path} py1.py -n {n}'"
        print(f"Running command for N={n}: {command}")
        stdout, stderr = run_remote_command(ssh, command)
        print(f"Output for N={n}:")
        print(stdout)
        if stderr:
            print(f"Error for N={n}:")
            print(stderr)

    # Check if all files exist and download them
    all_files_exist = True
    for n in n_values:
        image_path = f'{remote_path}/Chain3D_{n}.png'
        results_path = f'{remote_path}/results_{n}.txt'
        if not check_file_exists(sftp, image_path) or not check_file_exists(sftp, results_path):
            all_files_exist = False
            print(f"Files for N={n} are missing on the remote node.")
            break

    if all_files_exist:
        for n in n_values:
            download_file(sftp, f'{remote_path}/Chain3D_{n}.png', f'Chain3D_{n}.png')
            download_file(sftp, f'{remote_path}/results_{n}.txt', f'results_{n}.txt')

        # Check if files are in the local directory
        local_files_exist = all(os.path.exists(f'Chain3D_{n}.png') and os.path.exists(f'results_{n}.txt') for n in n_values)

        if local_files_exist:
            # Read N and h2 from each text file
            data = []
            for n in n_values:
                with open(f'results_{n}.txt', 'r') as f:
                    lines = f.readlines()
                    n_value = int(lines[0].split('=')[1])
                    h2_value = float(lines[1].split('=')[1])
                    data.append((n_value, h2_value))

            # Plot h2(N) ~ N
            n_array, h2_array = zip(*data)
            plt.figure(figsize=(10, 6))
            plt.plot(n_array, h2_array, 'o-')
            plt.xscale('log')
            plt.yscale('log')
            plt.xlabel('N')
            plt.ylabel('h2(N)')
            plt.title('h2(N) vs N')
            plt.savefig('h2_N_plot.png')
            plt.close()

            # Calculate scaling law h2(N) = N^v
            log_n = np.log(n_array)
            log_h2 = np.log(h2_array)
            v, _ = np.polyfit(log_n, log_h2, 1)
            print(f"Scaling law: h2(N) = N^{v:.4f}")

        else:
            print("Some files are missing in the local directory.")
    else:
        print("Some files are missing on the remote node.")

    # Close connections
    sftp.close()
    ssh.close()

if __name__ == "__main__":
    main()
