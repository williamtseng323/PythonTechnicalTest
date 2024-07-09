import sys
import os
import threading
import logging
from utils import load_config, monitor_directory, setup_logging
import pandas as pd

def main(config_path):
    """
    Main function to load the configuration and start monitoring directories.

    :param config_path: Path to the configuration file
    """
    # Load the configuration
    config = load_config(config_path)
    
    # Extract configuration details
    monitor_directories = config.get("monitor_directories", [])
    monitor_files = config.get("monitor_files", [])
    log_directory = config.get("log_directory", "logs")
    check_interval = config.get("params", {}).get("check_interval", 1)
    check_period = config.get("params", {}).get("check_period", 60)
    df = pd.DataFrame.from_dict(config["dataframes"]["example_df"],orient="tight")
    
    # Setup logging
    setup_logging(log_directory)

    # Start monitoring threads
    threads = []
    for directory in monitor_directories:
        if os.path.isdir(directory):
            thread = threading.Thread(target=monitor_directory, args=(directory, monitor_files, check_interval, check_period))
            thread.start()
            threads.append(thread)
        else:
            logging.error(f"Directory does not exist: {directory}")
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()

# Ensure the script is being run directly
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_config_file>")
        sys.exit(1)
    
    config_path = sys.argv[1]
    main(config_path)