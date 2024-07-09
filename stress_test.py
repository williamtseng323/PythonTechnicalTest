import os
import random
import string
import time
import numpy as np
import threading
import subprocess
import json

# Constants
NUM_FILES = 100
NUM_FOLDERS = 50
INTERVAL = 0.1
POISSON_MEAN = 1.6
CHECK_PERIOD = 60  # 1 minute

def generate_random_filename(length=10):
    """Generate a random filename with the specified length."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def create_random_file(directory, filename):
    """Create a random file in the specified directory."""
    file_path = os.path.join(directory, filename)
    with open(file_path, 'w') as f:
        f.write("This is a test file.")

def generate_files_and_folders(base_dir):
    """Generate random files and folders."""
    # Create base directory if it doesn't exist
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    # Create folders
    folders = [os.path.join(base_dir, f"folder_{i}") for i in range(NUM_FOLDERS)]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
    
    # Generate random filenames
    filenames = [generate_random_filename() for _ in range(NUM_FILES)]
    
    return folders, filenames

def create_files_randomly(folders, filenames):
    """Create random files in random folders."""
    start_time = time.time()
    while time.time() - start_time < CHECK_PERIOD:
        num_files_to_create = np.random.poisson(POISSON_MEAN)
        for _ in range(num_files_to_create):
            folder = random.choice(folders)
            filename = random.choice(filenames)
            create_random_file(folder, filename)
        time.sleep(INTERVAL)

def start_monitoring_program(config_path):
    """Start the monitoring program."""
    subprocess.run(["python", "main.py", config_path])

def main():
    # Generate files and folders
    base_dir = "test_data"
    folders, filenames = generate_files_and_folders(base_dir)
    
    # Write a configuration file for the monitoring program
    config = {
        "monitor_directories": folders,
        "monitor_files": filenames,
        "log_directory": "logs",
        "params": {
            "check_interval": 1,
            "check_period": CHECK_PERIOD  # 1 minute
        }
    }
    
    config_path = "stress_test_config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)
    
    # Start the monitoring program in a separate thread
    monitoring_thread = threading.Thread(target=start_monitoring_program, args=(config_path,))
    monitoring_thread.start()
    
    # Start creating files randomly
    create_files_randomly(folders, filenames)

if __name__ == "__main__":
    main()