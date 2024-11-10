# model_test.py

import numpy as np
import tensorflow as tf
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Load the TFLite model
interpreter = tf.lite.Interpreter(model_path="optimized_autoencoder.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load the scaler used during training (from the same CSV file used for training)
data = pd.read_csv("/home/ishanurgaonkar/Downloads/system_metrics_dynamic.csv")  # Update with your CSV filename
scaler = MinMaxScaler()
scaler.fit(data[['cpu_load', 'cpu_freq', 'ram_usage']])

# Function to detect anomalies in real-time
def detect_anomaly(data_point):
    cpu_load, cpu_freq, temperature, ram_usage = data_point

    # Scale the data point before feeding it to the model
    data_point_scaled = scaler.transform([[cpu_load, cpu_freq, ram_usage]])

    # Run the autoencoder for reconstruction (only for scaled features)
    interpreter.set_tensor(input_details[0]['index'], np.array(data_point_scaled, dtype=np.float32))
    interpreter.invoke()
    reconstructed_data = interpreter.get_tensor(output_details[0]['index'])[0]

    # Calculate MSE (Mean Squared Error)
    mse = np.mean(np.power(data_point_scaled - reconstructed_data, 2))

    # Print MSE for debugging
    print(f"Input: {data_point}")
    print(f"Reconstructed: {reconstructed_data}")
    print(f"MSE: {mse}")

    # Check temperature anomaly (direct if-else check)
    if temperature > 55:
        print(f"Temperature anomaly detected: {temperature}°C")
        return True

    # Check for RAM usage anomaly (greater than 3500 MB)
    if ram_usage > 3500:  # New RAM threshold condition
        print(f"RAM anomaly detected: {ram_usage} MB")
        return True

    # Check for high CPU load anomaly (greater than 80%)
    if cpu_load > 80:  # High CPU load condition
        print(f"High CPU load detected: {cpu_load}%")
        return True

    # Calculate anomaly score based on weighted conditions
    anomaly_score = 0
    if cpu_load > 80:  # High CPU load condition
        anomaly_score += 2
    if ram_usage > 3 * 1024:  # High RAM usage condition (3 GB)
        anomaly_score += 2
    if cpu_freq < 1000 or cpu_freq > 2800:  # CPU frequency condition
        anomaly_score += 1

    # Detect anomaly if score exceeds threshold or MSE is high
    mse_threshold = 0.2  # Adjust threshold to reduce false positives (increased threshold)
    if anomaly_score >= 4 or mse > mse_threshold:  # Adjust MSE threshold based on testing
        print(f"Anomaly Detected based on MSE! (MSE: {mse})")
        return True

    return False

# Function to read the input data from the file
def read_input_file(file_path):
    try:
        with open(file_path, 'r') as f:
            data = f.read().strip()
            return list(map(float, data.split(',')))
    except Exception as e:
        print(f"Error reading input file: {e}")
        return None

# Main loop to read input from the file and detect anomalies
if __name__ == "__main__":
    input_data = read_input_file('input_data.txt')
    if input_data:
        is_anomaly = detect_anomaly(input_data)
        if is_anomaly:
            print("Anomaly detected in the input data.")
        else:
            print("No anomaly detected in the input data.")
    else:
        print("No input data found.")
