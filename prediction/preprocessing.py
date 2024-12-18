import pandas as pd


def preprocess_data(data):
    """
    Preprocess the data to add lag features and rolling averages for irregular time intervals.
    """
    # Ensure 'timestamp' is a datetime object
    data['timestamp'] = pd.to_datetime(data['timestamp'])

    # Sort data by timestamp to ensure order
    data = data.sort_values(by='timestamp')

    # Add lag features directly without resampling
    data['temp_lag1'] = data['temperature_value'].shift(1)
    data['temp_lag2'] = data['temperature_value'].shift(2)

    # Calculate rolling mean (window = 3)
    data['temp_rolling_mean'] = data['temperature_value'].rolling(window=3).mean()

    # Convert motion_status to integer (if boolean)
    data['motion_status'] = data['motion_status'].astype(int)

    # Drop rows with NaN values (caused by lags and rolling mean)
    return data.dropna()
