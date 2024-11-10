import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras import regularizers
import tensorflow as tf

# Load data from CSV file (ensure the CSV has 'cpu_load', 'cpu_freq', 'ram_usage', and 'temperature' columns)
data = pd.read_csv("/home/ishanurgaonkar/Downloads/system_metrics_dynamic.csv")  # Update with your CSV filename

# Data preprocessing: Only scale 'cpu_load', 'cpu_freq', and 'ram_usage'
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data[['cpu_load', 'cpu_freq', 'ram_usage']])

# Define autoencoder model
input_dim = data_scaled.shape[1]
encoding_dim = 2  # Adjust based on the model size you need
input_layer = Input(shape=(input_dim,))
encoder = Dense(encoding_dim, activation="relu", activity_regularizer=regularizers.l1(10e-5))(input_layer)
decoder = Dense(input_dim, activation="sigmoid")(encoder)
autoencoder = Model(inputs=input_layer, outputs=decoder)

autoencoder.compile(optimizer='adam', loss='mse')

# Train the autoencoder
autoencoder.fit(data_scaled, data_scaled, epochs=50, batch_size=32, validation_split=0.1, verbose=1)

# Save the trained model
autoencoder.save('optimized_autoencoder.h5')

# Convert to TFLite model with quantization
converter = tf.lite.TFLiteConverter.from_keras_model(autoencoder)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()

# Save the TFLite model for deployment on STM32
with open("optimized_autoencoder.tflite", "wb") as f:
    f.write(tflite_model)

# Load the TFLite model for testing
interpreter = tf.lite.Interpreter(model_path="optimized_autoencoder.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Function to detect anomalies in real-time
def detect_anomaly(data_point):
    # Extract features
    cpu_load, cpu_freq, temperature, ram_usage = data_point

    # Ensure data point is passed as a 2D array (fix for MinMaxScaler warning)
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

# Function to handle user input for testing
def get_user_input():
    try:
        cpu_load = float(input("Enter CPU load (%): "))
        cpu_freq = float(input("Enter CPU frequency (MHz): "))
        temperature = float(input("Enter temperature (°C): "))
        ram_usage = float(input("Enter RAM usage (MB): "))
        return [cpu_load, cpu_freq, temperature, ram_usage]
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        return None

# Test the model with user input
while True:
    test_data = get_user_input()
    if test_data:
        is_anomaly = detect_anomaly(test_data)
        if is_anomaly:
            print("Anomaly detected in the input data.")
        else:
            print("No anomaly detected in the input data.")
    else:
        print("Please enter valid input values.")