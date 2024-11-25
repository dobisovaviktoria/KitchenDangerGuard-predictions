import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
import config

# Load motion and temperature data from the database
kdg_data = config.engine
motion_df = pd.read_sql('SELECT * FROM motion_data', kdg_data)
temperature_df = pd.read_sql('SELECT * FROM temperature_data', kdg_data)

# Check for missing values and drop them
motion_df.dropna(inplace=True)
temperature_df.dropna(inplace=True)

# Convert timestamps to datetime
motion_df['motion_timestamp'] = pd.to_datetime(motion_df['motion_timestamp'])
temperature_df['temp_timestamp'] = pd.to_datetime(temperature_df['temp_timestamp'])

# Merge datasets based on nearest timestamps
combined_data = pd.merge_asof(
    temperature_df.sort_values('temp_timestamp'),
    motion_df.sort_values('motion_timestamp'),
    left_on='temp_timestamp',
    right_on='motion_timestamp',
    direction='nearest'
)

# Feature engineering
combined_data['time_since_last_motion'] = (
    combined_data['motion_timestamp'] - combined_data['motion_timestamp'].shift()
).dt.total_seconds().fillna(0)

# Define features (X) and labels (y)
X = combined_data[['temp_value', 'motion_sensor_status', 'time_since_last_motion']]
combined_data['unattended'] = ~combined_data['motion_sensor_status']
y = combined_data['unattended'].astype(int)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)
print("Model training complete.")

# Evaluate the model
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Save the trained model
joblib.dump(model, 'unattended_stove_model.pkl')
print("Model saved to 'unattended_stove_model.pkl'.")

# Load the model for predictions
model = joblib.load('unattended_stove_model.pkl')
print("Model loaded successfully.")

# Example input data for prediction
# Fetch new data from the database and ensure it matches the feature names
new_data = pd.DataFrame([[45.6, 0, 600]], columns=['temp_value', 'motion_sensor_status', 'time_since_last_motion'])

# Make a prediction
prediction = model.predict(new_data)

# Interpret the prediction
print("Prediction:", "Unattended" if prediction[0] == 1 else "Attended")
