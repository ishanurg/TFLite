# System Metrics Collection for Anomaly Detection on Raspberry Pi 5

**Author:** Ishan Urgaonkar  

## Project Overview

This project simulates and collects system metrics such as CPU load, CPU frequency, RAM usage, and CPU temperature on a Raspberry Pi 5 for anomaly detection. These metrics are gathered in real-time over varying CPU load levels, which are then saved to a CSV file for analysis. The data collected can be used to train machine learning models (e.g., autoencoders) for detecting system anomalies and ensuring system health.

The following features are included:
- CPU load simulation for different levels (from 10% to 90%).
- Real-time collection of CPU frequency, temperature, and RAM usage.
- Logging system metrics to a CSV file (`system_metrics_dynamic.csv`).
- Data collection runs at different CPU load levels for 3-minute intervals.

This setup is ideal for researchers or engineers looking to gather system performance data for machine learning or anomaly detection tasks.

## Key Features

- **Simulated CPU Load:** Runs CPU load at different levels for system performance testing.
- **System Metrics Logging:** Records CPU load, frequency, temperature, and RAM usage.
- **CSV Output:** Saves system metrics data to `system_metrics_dynamic.csv` for analysis.
- **Cross-platform Support:** Designed to run on Raspberry Pi 5 but can be adapted to other Linux-based systems.

## Components Used

- **Raspberry Pi 5:** SBC for data collection and simulation.
- **Python Libraries:**
  - `psutil`: For CPU load, memory, and frequency monitoring.
  - `subprocess`: To read CPU temperature.
  - `multiprocessing`: To simulate CPU load via parallel processing.
  - `csv`: To store data in CSV format.
  - `time`: For interval timing and process control.
- **Output File:** `system_metrics_dynamic.csv`.

## GitHub Repository

You can access the full project, including the code, via the following [GitHub Repository](https://github.com/ishanurg/SystemMetricsCollection).

## Project Workflow

### Step 1: Create a Virtual Environment

To ensure dependencies are installed in an isolated environment, it’s recommended to create a virtual environment first. Run the following commands to create and activate the environment:
 
 Install virtualenv if not installed
```bash
pip install virtualenv
```
# Create a virtual environment named "dataset"
```bash
python3 -m venv dataset
```
# Activate the virtual environment
```bash
cd dataset
source bin/activate
```
Step 2: Clone the Repository
Clone the repository to your Raspberry Pi 5 (or local machine) to access the code:

```bash
git clone -b master-pi https://github.com/ishanurg/TFLite.git
```
Step 3: Install Dependencies
Install the required Python libraries by running the following command in your virtual environment:

```bash
pip install -r requirements.txt
```
```bash
pip install psutil
```
Step 4: Run the Data Collection Script
The data_collection.py script collects system metrics at different CPU load levels (from 10% to 90%) and logs them to a CSV file.

Run the script using:

```bash
python data_collection.py
```
The system will:
Simulate CPU load levels in the range of 10% to 90%.
Collect the following metrics every second:
CPU Load (%)
CPU Frequency (MHz)
CPU Temperature (°C)
RAM Usage (MB)
The data will be saved in a CSV file called system_metrics_dynamic.csv.
Step 5: Check the Output
After the script finishes running, you will have a CSV file called system_metrics_dynamic.csv containing the system metrics data. The file will include the following columns:

Timestamp: The time the metric was logged.
CPU Load (%): The simulated CPU load during that timestamp.
CPU Frequency (MHz): The frequency of the CPU at that time.
CPU Temperature (°C): The temperature of the CPU.
RAM Usage (MB): The amount of RAM used at that time.
Step 6: Stop the Script
You can stop the script anytime by pressing Ctrl+C in the terminal. It will safely terminate the data collection process.

Code Structure
The project consists of the following key files:

data_collection.py
The main script that collects system metrics and logs them to a CSV file.
Includes functions to simulate CPU load, read CPU frequency and temperature, and monitor RAM usage.
Logs the collected data to system_metrics_dynamic.csv.
requirements.txt
Contains a list of required Python libraries for the project (e.g., psutil).
system_metrics_dynamic.csv
CSV file where system metrics are logged. The data includes:
Timestamp
CPU Load (%)
CPU Frequency (MHz)
CPU Temperature (°C)
RAM Usage (MB)
How to Run the Project
1. Clone the repository
```bash
git clone -b master-pi https://github.com/ishanurg/TFLite.git
```
2. Set up a Virtual Environment
```bash
virtualenv env
```
# Activate the environment
```bash
source env/bin/activate
```
3. Install Dependencies
```bash
pip install -r requirements.txt
```
4. Run the Data Collection Script
```bash
python dataset.py
```
5. Check the Output
The system metrics will be logged in the system_metrics_dynamic.csv file. You can open this file with a spreadsheet application or analyze it programmatically.

6. Stop the Script
You can stop the script anytime by pressing Ctrl+C in the terminal.


#References
psutil Documentation: https://psutil.readthedocs.io
Raspberry Pi 5 Documentation: https://www.raspberrypi.org/documentation/
Subprocess Module (Python): https://docs.python.org/3/library/subprocess.html


---

### Key Points in the README:

1. **Virtual Environment Setup**: Instructions to create a virtual environment using `virtualenv` for isolated dependency management.
2. **Step-by-Step Guide**: Includes steps to clone the repo, install dependencies, run the data collection script, and check the results.
3. **CSV File Output**: Describes the contents of the CSV file that is generated and how to interpret it.
4. **Key Features**: Highlights the main functionalities of the system, such as CPU load simulation and metrics logging.



