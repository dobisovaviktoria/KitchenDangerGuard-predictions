import pandas as pd
import numpy as np
import config

# Load motion and temperature data
kdf_data = config.engine
motion_df = pd.read_sql('SELECT * FROM motion_data', kdf_data)
temperature_df = pd.read_sql('SELECT * FROM temperature_data', kdf_data)

# Check for missing values
print(motion_df.isnull().sum())
print(temperature_df.isnull().sum())

# Drop missing rows or fill them
motion_df.dropna(inplace=True)
temperature_df.dropna(inplace=True)

# Convert timestamps to datetime
motion_df['motion_timestamp'] = pd.to_datetime(motion_df['motion_timestamp'])
temperature_df['temp_timestamp'] = pd.to_datetime(temperature_df['temp_timestamp'])

print(motion_df)
print(temperature_df)