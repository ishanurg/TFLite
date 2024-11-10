import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras import regularizers
import tensorflow as tf

# Load data from CSV file (ensure the CSV has 'cpu_load', 'cpu_freq', 'temperature', 'ram_usage' columns)
data = pd.read_csv("/home/ishanurgaonkar/Downloads/system_metrics_dynamic.csv")  # Update with your CSV filename

# Data preprocessing: Only select columns for scaling (ignore 'timestamp')
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data[['cpu_load', 'cpu_freq', 'temperature', 'ram_usage']])

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

# Set thresholds for real-time anomaly detection
high_temp_threshold = 55
high_cpu_usage_threshold = 80
high_ram_usage_threshold = 3 * 1024  # 3 GB
cpu_freq_lower_threshold = 1500
cpu_freq_upper_threshold = 2800

# Load the TFLite model for testing
interpreter = tf.lite.Interpreter(model_path="optimized_autoencoder.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Function to detect anomalies in real-time
def detect_anomaly(data_point):
    # Scale and preprocess data (ignore the timestamp column)
    data_point_scaled = scaler.transform([data_point])  # Don't include timestamp, use only the features
    
    # Run the autoencoder for reconstruction
    interpreter.set_tensor(input_details[0]['index'], np.array(data_point_scaled, dtype=np.float32))
    interpreter.invoke()
    reconstructed_data = interpreter.get_tensor(output_details[0]['index'])[0]
    mse = np.mean(np.power(data_point_scaled - reconstructed_data, 2))

    # Calculate anomaly score based on weighted conditions
    anomaly_score = 0
    
    # High priority conditions
    if data_point[0] > high_cpu_usage_threshold:  # cpu_load condition
        anomaly_score += 3
    if data_point[2] > high_temp_threshold:  # temperature condition
        anomaly_score += 3
    if data_point[3] > high_ram_usage_threshold:  # ram_usage condition
        anomaly_score += 2

    # CPU frequency condition (low priority)
    if data_point[1] < cpu_freq_lower_threshold:  # cpu_freq drops below threshold
        anomaly_score += 1
    elif data_point[1] > cpu_freq_upper_threshold:  # cpu_freq goes above threshold
        anomaly_score += 1

    # Detect anomaly if score exceeds threshold or MSE is high
    if anomaly_score >= 4 or mse > 1:  # Adjust threshold based on testing
        print("Anomaly Detected!")
        return True
    return False

# Example: Test the model with an input (only providing the relevant feature values)
test_data = [55, 2000, 48, 1100]  # cpu_load, cpu_freq, temperature, ram_usage (timestamp is ignored)
is_anomaly = detect_anomaly(test_data)

if is_anomaly:
    print("Anomaly detected in the test data.")
else:
    print("No anomaly detected.")
