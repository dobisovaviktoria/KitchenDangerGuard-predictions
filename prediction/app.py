from flask import Flask, jsonify
from database import fetch_data, fetch_all_devices
from model import train_model, predict_future

app = Flask(__name__)

# Train models for all devices
def train_all_models():
    devices = fetch_all_devices()  # Fetch all device IDs
    # Loop through each device, fetch the data and train the model
    for device_id in devices:
        data = fetch_data(device_id)  # Fetch the data for the specific device
        train_model(device_id, data)  # Train and save the model for the device

# Call the function to train all models (this will run when the script starts)
train_all_models()

# Predict future values for a specific device
@app.route('/predict/<arduino_id>', methods=['GET'])
def predict(arduino_id):
    # Fetch the data for the Arduino device
    data = fetch_data(arduino_id)

    # Get all predictions and their timeframes
    predictions, timeframes = predict_future(arduino_id, data, future_steps=5)

    # Debugging: Log all predictions and timestamps
    print("All Predictions and Timestamps:")
    for temp, timeframe in zip(predictions, timeframes):
        print(f"Temperature: {temp}, Timestamp: {timeframe}")

    # Filter for dangerous predictions within the desired time range
    hazard_threshold = 50.0  #  threshold
    max_future_time = 120  # Maximum 120 minutes from the latest timestamp

    filtered_results = [
        {"temperature": temp, "timeframe": str(timeframe)}
        for temp, timeframe in zip(predictions, timeframes)
        if temp > hazard_threshold and (timeframe - data['timestamp'].iloc[-1]).total_seconds() <= max_future_time * 60
    ]

    # Take only the first dangerous prediction, if any
    dangerous_prediction = filtered_results[0] if filtered_results else None

    # Build the response structure
    response = {
        "arduino_id": arduino_id,
        "future_prediction": dangerous_prediction,  # Send only the first dangerous prediction
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)  # This line starts the Flask app with debugging enabled