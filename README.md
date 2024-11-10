# Anomaly Detection Using Machine Learning Model for System Performance Monitoring

**Author:** Ishan Urgaonkar  
**Reg No:** 22BEC0702  
**Subject:** AI & ML

## Project Overview

Anomaly detection in Single-Board Computers (SBCs) and embedded systems is crucial for ensuring stable performance in real-time applications. This project utilizes machine learning techniques to detect anomalies based on dynamic system metrics such as CPU load, RAM usage, CPU frequency, and temperature. The system is built to monitor SBCs like the Raspberry Pi 5 and is deployed to the STM32 H7 Nucleo microcontroller for edge inference.

This project includes:
- Data collection from Raspberry Pi 5 using system monitoring tools.
- An autoencoder-based machine learning model for anomaly detection.
- Conversion of the trained model to TensorFlow Lite format.
- Deployment on the STM32 H7 Nucleo microcontroller with real-time anomaly detection feedback via an LED indicator.

## Key Features

- **Real-Time Anomaly Detection:** Detects anomalies like high CPU load, memory issues, or overheating.
- **Edge Deployment:** The trained model is optimized and deployed on resource-constrained devices like the STM32 H7 Nucleo microcontroller.
- **Machine Learning Model:** Uses an autoencoder for unsupervised anomaly detection, which adapts to normal system behavior without needing labeled data.
- **Efficient and Scalable:** TensorFlow Lite optimizes the model for efficient deployment on embedded devices.

## Components Used

- **Raspberry Pi 5:** SBC for data collection.
- **STM32 H7 Nucleo 144:** Microcontroller for model inference.
- **STM32 Cube AI:** Toolchain for model optimization and deployment.
- **TensorFlow Lite (TFLite):** Framework for converting and deploying the model on embedded systems.
- **Python Libraries:**
  - `psutil`: For CPU load and RAM usage monitoring.
  - `subprocess`: For fetching CPU temperature.
  - `multiprocessing`: For simulating system load variations.
  - `pandas`, `numpy`: For data manipulation and processing.
  - `scikit-learn`: For scaling the data.
- **CSV File:** Stores the collected system metrics data.

## GitHub Repository

Access the full project, including code and detailed implementation, via the following [GitHub Repository](https://github.com/ishanurg/TFLite.git).

## Project Workflow

### Step 1: Data Collection

- The system metrics (CPU load, RAM usage, CPU frequency, and temperature) are collected from the Raspberry Pi 5.
- Tools used:
  - `psutil`: For CPU load and RAM usage.
  - `subprocess`: To read CPU temperature.
  - `multiprocessing`: To simulate different load levels.
- The data is stored in a CSV file (`system_metrics_dynamic.csv`) for further processing.

### Step 2: Model Training

- **Autoencoder-based Model:**
  - **Why Autoencoder?** Autoencoders are ideal for anomaly detection in unsupervised settings. They learn the normal system behavior and can flag anomalies based on the reconstruction error.
  - **Model Architecture:**
    - Encoder and decoder architecture compresses input features (CPU load, frequency, RAM usage).
    - Uses Mean Squared Error (MSE) loss to minimize reconstruction error.
    - The model is trained on the dataset using scaled values for CPU load, CPU frequency, and RAM usage.
- **Model Training Process:**
  - Data preprocessing: MinMax scaling for CPU load, frequency, and RAM usage.
  - The autoencoder model is trained using TensorFlow/Keras.
  - The trained model is saved and converted to `.h5` format.

### Step 3: Model Conversion to TensorFlow Lite

- The trained model is converted to TensorFlow Lite format (`.tflite`) for efficient deployment on resource-constrained devices like the STM32 Nucleo microcontroller.
- **Model Quantization:** Reduces the model size for optimal performance on embedded devices.

### Step 4: Model Deployment on STM32 H7 Nucleo 144

- Using **STM32 Cube AI**, the converted TensorFlow Lite model is deployed to the STM32 H7 Nucleo microcontroller.
- The microcontroller performs inference on the system metrics and indicates anomaly detection via an LED blink (green for no anomaly, red for anomaly).
  
### Step 5: Anomaly Detection

- During inference, the system calculates the reconstruction error (MSE) between the input data and the model's reconstruction.
- If the error exceeds a predefined threshold, an anomaly is flagged.
- Additional checks for system metrics (e.g., temperature, CPU load) are included to detect known issues that may not be captured by the model alone.

## Code Structure

The project consists of the following key files and directories:

### `data_collection.py`
- Script for collecting system metrics from Raspberry Pi 5 (CPU load, RAM usage, temperature).
- Saves collected data in a CSV file.

### `model_training.py`
- Defines and trains the autoencoder model for anomaly detection.
- Scales the data and trains the model using Mean Squared Error (MSE).
- Converts the trained model to TensorFlow Lite format.

### `anomaly_detection.py`
- Contains functions for detecting anomalies based on the trained model and system metrics.
- Includes threshold-based checks for temperature, CPU load, and RAM usage.

### `deployment_code/`
- Contains code for deployment on the STM32 Nucleo microcontroller.
- The `main.c` file handles the model inference and LED feedback.

## How to Run the Project

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ishanurg/TFLite.git
   cd TFLite
