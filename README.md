# Centerline Python Technical Test
This repository serves as a python technical test for the role - Centerline Trading Analyst. <br>
Solely developed by TSENG, Wai Yin

# Development Environment and Required Python Version
It was developed in Python 3.10.4 and should work for Python 3.10.x

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/williamtseng323/PythonTechnicalTest
    ```
2. (Optional) Initialize a venv
    ```sh
    python -m venv venv
    venv/Scripts/activate
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Main Feature: Monitoring Program

The monitoring program observes the specified directories for the appearance of specific file names and logs these activities. <br>
The files are not bounded to any directory. The system continously match any file name to the specified file list as queries are as efficient as **O(1)** in my implementation.

1. The monitoring program is executed, specify the path to config file (mandatory):
    ```sh
    python -u main.py config.json
    ```
## Logs
The log records the appearance of the files and timestamps. They are typically stored in logs unless you specified another location to store these logs.
### Sample Logs

- 2024-07-09 21:24:46,226 - INFO - File monitor_file_1.txt appeared in directory monitor_directory_2
- 2024-07-09 21:24:48,235 - INFO - File monitor_file_2.csv appeared in directory monitor_directory_1

## Configuration File

The configuration for the monitoring program is stored in a `config.json` file. The configuration includes:

- Directories to monitor : "monitor_directories"
- Names of the files to monitor : "monitor_files"
- Logging directory : "log_directory"
- Monitoring parameters (check interval and check period) : "params"
- Other variables like pandas DataFrames, stored in orient="tight"

Example `config.json`:
```json
{
    "monitor_directories": ["test_data/folder_0", "test_data/folder_1", ...],
    "monitor_files": ["file1.txt", "file2.txt", ...],
    "log_directory": "logs",
    "params": {
        "check_interval": 1,
        "check_period": 60
    },
    "dataframes": {
        "example_df": {
            "columns": ["open", "high","low","close","volume"],
            "index": [0, 1],
            "data": [[1.1,1.2,1.0,1.05,10000], [1.05,1.1,0.9,0.95,20000]],
            "index_names":["ohlc_id"],
            "column_names":["price_type"]
        }
    }
}
```
# Optimization
There are two optimizations I applied. 
1. I used **multi-threading** to manage different folders simultaneously. Parallel programming not used as to reserve system resources.
2. I applied **hash set** to achieve an average **O(1)** search for whether an appeared file belongs to our watchlist. Compared to linear search O(n) or binary search O(log n), I gave up all the unnecessary information in exchange for efficiency. Low level optimization is not economical due to the nature of Python.

## Assumptions
1. The project assumes config files are created manually. 
2. DataFrame is formatted with orient="tight".
3. The script has permission to read the provided paths and files.
4. User calculates the detect period and detect interval.
5. Extensions are easily possible but still require extra codes.
6. Tested in MacOS (M1 Silicon) and Windows.
7. frozenset has same efficiency as set in Python.