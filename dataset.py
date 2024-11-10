import time
import csv
import psutil
import subprocess
import os
import random
from datetime import datetime
import multiprocessing

# CSV file setup
csv_filename = "system_metrics_dynamic.csv"

# CPU load levels for 3-minute intervals
load_levels = [10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90]
duration_per_level = 100  # 3 minutes in seconds
max_ram_usage = 4 * 1024  # Max RAM usage in MB (4 GB)

# CPU frequency adjustment range for more variation
freq_variation_range = 800  # +/- 200 MHz for better frequency diversification

# Function to apply CPU load in a separate process
def apply_cpu_load(target_load):
    start_time = time.time()
    while True:
        active_time = 0.1 * (target_load / 100.0)
        idle_time = 0.1 - active_time
        loop_start = time.time()
       
        # Active phase
        while (time.time() - loop_start) < active_time:
            pass  # Busy-wait to simulate load
       
        # Idle phase
        time.sleep(idle_time)

        # Exit if the time is up
        if time.time() - start_time > duration_per_level:
            break

# Function to get CPU temperature
def get_temperature():
    try:
        temp = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8").strip()
        return float(temp.split("=")[1].replace("'C", "").strip())
    except (subprocess.CalledProcessError, ValueError) as e:
        print(f"Error reading temperature: {e}")
        return None

# Function to simulate more diversified CPU frequency changes
def simulate_frequency_variation():
    base_freq = psutil.cpu_freq().current  # Get base CPU frequency
    return base_freq + random.uniform(-freq_variation_range, freq_variation_range)

# Function to adjust RAM usage within the defined limit
def simulate_ram_usage():
    base_usage = psutil.virtual_memory().used / 1024 / 1024  # in MB
    if base_usage < max_ram_usage:
        return random.uniform(base_usage, max_ram_usage)
    return base_usage

# Function to gather and log system metrics
def gather_metrics(writer, load):
    cpu_freq = simulate_frequency_variation()  # Simulate frequency variation
    cpu_temp = get_temperature()  # Get CPU temperature
    ram_usage = simulate_ram_usage()  # Adjust and get RAM usage
    writer.writerow([datetime.now(), load, cpu_freq, cpu_temp, ram_usage])  # Log metrics

# Main loop
def main():
    file_exists = os.path.isfile(csv_filename)
    with open(csv_filename, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["Timestamp", "CPU Load (%)", "CPU Frequency (MHz)", "CPU Temp (°C)", "RAM Usage (MB)"])

        for load in load_levels:
            print(f"Running with CPU load set to {load}% for {duration_per_level} seconds.")

            # Create a separate process to apply CPU load
            load_process = multiprocessing.Process(target=apply_cpu_load, args=(load,))
            load_process.start()

            # Log metrics every second
            start_time = time.time()
            while time.time() - start_time < duration_per_level:
                gather_metrics(writer, load)  # Pass the load directly to the function
                csvfile.flush()  # Ensure data is written immediately
                time.sleep(1)

            # Terminate the CPU load process after 3 minutes
            load_process.terminate()
            load_process.join()

            # Small pause before moving to the next load level
            time.sleep(2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Stopped by the user.")
    except Exception as e:
        print(f"Unexpected error: {e}")
