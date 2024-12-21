import os
import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from preprocessing import preprocess_data

hazard_threshold=170

# Directory for saving models
MODEL_DIR = "./USER_MODELS"  # Correct directory where models will be saved
os.makedirs(MODEL_DIR, exist_ok=True)  # Create the directory if it doesn't exist

# Train a model for a specific Arduino device
def train_model(arduino_id, data):
    # Preprocess data
    data = preprocess_data(data)
    if data is not None:
        # Define features and target
        X = data[['temp_lag1', 'temp_lag2', 'temp_rolling_mean', 'motion_status']]
        y = data['temperature_value']

        # Train/Test split
        train_size = int(len(X) * 0.8)
        X_train, y_train = X.iloc[:train_size], y.iloc[:train_size]
        X_test, y_test = X.iloc[train_size:], y.iloc[train_size:]

        # Train model
        model = RandomForestRegressor(random_state=42)
        model.fit(X_train, y_train)

        # Correctly save the model in the USER_MODELS directory
        model_filename = os.path.join(MODEL_DIR, f"predict_kitchen_hazard_model_{arduino_id}.pkl")
        joblib.dump(model, model_filename)
        print(f"Model for device {arduino_id} trained and saved as {model_filename}.")



def predict_future(arduino_id, data, future_steps=5):
    """
    Predict future values for a device with irregular time intervals.
    """
    print("Data before preprocessing:")
    print(data.head())

    # Preprocess data: add lags and rolling mean
    data = preprocess_data(data)

    print("Data after preprocessing:")
    print(data.head())

    # Check if the required features are available
    required_features = ['temp_lag1', 'temp_lag2', 'temp_rolling_mean', 'motion_status']
    for feature in required_features:
        if feature not in data.columns:
            raise KeyError(f"Missing required feature '{feature}' in the data")

    # Load the trained model for this arduino_id
    model_path = os.path.join(MODEL_DIR, f"predict_kitchen_hazard_model_{arduino_id}.pkl")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file {model_path} not found.")

    # Attempt to load the model and print confirmation
    model = joblib.load(model_path)
    print(f"Model for Arduino ID {arduino_id} loaded successfully.")

    # Extract the most recent data point (reshaped to 2D for model prediction)
    latest_data = data.loc[
        data.index[-1], ['temp_lag1', 'temp_lag2', 'temp_rolling_mean', 'motion_status']].values.reshape(1, -1)
    print(f"Latest data for prediction: {latest_data}")

    # Get the last known timestamp
    last_timestamp = data['timestamp'].iloc[-1]  # Last known timestamp
    print(f"Last timestamp: {last_timestamp}")

    # Calculate the time difference between the last two data points
    if len(data) > 1:
        time_diff = (data['timestamp'].iloc[-1] - data['timestamp'].iloc[-2]).total_seconds() / 60  # in minutes
    else:
        time_diff = 10  # Default to 10 minutes if there's not enough data
    print(f"Time difference for predictions: {time_diff} minutes")

    predictions = []
    timeframes = []

    # Predict future values based on the time difference
    for step in range(future_steps):

            # Predict the next temperature
            print(f"Model input for step {step + 1}: {latest_data}")
            next_temp = model.predict(latest_data)[0]
            predictions.append(next_temp)

            # Calculate the next timestamp using the time difference
            next_timestamp = last_timestamp + pd.Timedelta(minutes=time_diff)
            timeframes.append(next_timestamp)

            print(f"Prediction step {step + 1}")
            print(f"Predicted temperature for step {step + 1}: {next_temp}")
            print(f"Timestamp for step {step + 1}: {next_timestamp}")

            # Update lag features for the next iteration
            latest_data = latest_data.flatten()
            latest_data = np.roll(latest_data, 1)  # Shift features to the right
            latest_data[0] = next_temp  # Replace temp_lag1 with the predicted temperature
            latest_data = latest_data.reshape(1, -1)  # Ensure proper shape

            # Update the last timestamp for the next prediction
            last_timestamp = next_timestamp


    return predictions,timeframes

