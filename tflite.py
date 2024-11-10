import tensorflow as tf

model_path = "/home/ishanurgaonkar/Desktop/AI-ML/optimized_autoencoder.h5"
autoencoder = tf.keras.models.load_model(model_path, custom_objects={'mse': tf.keras.losses.MeanSquaredError()})


# Convert the Keras model to TensorFlow Lite format with optimizations (quantization)
converter = tf.lite.TFLiteConverter.from_keras_model(autoencoder)
converter.optimizations = [tf.lite.Optimize.DEFAULT]  # Apply quantization
tflite_model = converter.convert()

# Save the TensorFlow Lite model
tflite_model_path = 'optimized_autoencoder.tflite'
with open(tflite_model_path, 'wb') as f:
    f.write(tflite_model)

print("TensorFlow Lite model saved:", tflite_model_path)
