import json
import os
import threading
import time
import logging
import platform
import subprocess
from datetime import datetime

def setup_logging(log_directory):
    """
    Setup logging to output to a unique file in the specified directory for each session.
    
    :param log_directory: Directory to store the log file
    """
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    # Generate a unique log file name based on the current date and time
    log_file = os.path.join(log_directory, f'session_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def load_config(config_path):
    """
    Load and parse the configuration file.
    
    :param config_path: Path to the configuration file
    :return: Parsed configuration as a dictionary
    """
    try:
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        return config
    except FileNotFoundError:
        logging.error(f"Configuration file not found: {config_path}")
        raise
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from the configuration file: {config_path}")
        raise

def monitor_directory(directory, monitor_files, interval, check_period):
    """
    Monitor a directory for the appearance of specific files.
    
    :param directory: Directory to monitor
    :param monitor_files: Set of files to monitor for
    :param interval: Interval between checks
    :param check_period: Total time to monitor the directory
    """
    monitor_files_set = set(monitor_files)
    start_time = time.time()
    try:
        while time.time() - start_time < check_period:
            existing_files = os.listdir(directory)
            for file in existing_files:
                if file in monitor_files_set:
                    handle_file_appearance(directory, file)
                    monitor_files_set.remove(file)  # Remove the file from the set once it is found
            if not monitor_files_set:
                break  # Stop monitoring if all files have been found
            time.sleep(interval)
    except Exception as e:
        logging.error(f"Error monitoring directory {directory}: {e}")

def handle_file_appearance(directory, file):
    """
    Handle the appearance of a monitored file.
    
    :param directory: Directory where the file appeared
    :param file: The file that appeared
    """
    logging.info(f"File {file} appeared in directory {directory}")
    notify_user(directory, file)

def notify_user(directory, file):
    """
    Send a system notification when a monitored file appears.
    
    :param directory: Directory where the file appeared
    :param file: The file that appeared
    """
    notification_title = "File Alert"
    notification_message = f"The file '{file}' has appeared in '{directory}'"
    
    if platform.system() == "Darwin":  # macOS
        command = f'display notification "{notification_message}" with title "{notification_title}"'
        subprocess.run(["osascript", "-e", command])
    else:
        try:
            from plyer import notification
            notification.notify(
                title=notification_title,
                message=notification_message,
                app_name='Directory Monitor'
            )
        except ImportError:
            logging.error("Notification could not be sent. Please ensure 'plyer' is installed.")