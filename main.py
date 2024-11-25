import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import config

# Load motion and temperature data
kdg_data = config.engine
motion_df = pd.read_sql('SELECT * FROM motion_data', kdg_data)
temperature_df = pd.read_sql('SELECT * FROM temperature_data', kdg_data)

# Check for missing values
print("Missing Values in Motion Data:")
print(motion_df.isnull().sum())
print("\nMissing Values in Temperature Data:")
print(temperature_df.isnull().sum())

# Drop missing rows or fill them
motion_df.dropna(inplace=True)
temperature_df.dropna(inplace=True)

# Convert timestamps to datetime
motion_df['motion_timestamp'] = pd.to_datetime(motion_df['motion_timestamp'])
temperature_df['temp_timestamp'] = pd.to_datetime(temperature_df['temp_timestamp'])

# Show basic information and summary statistics
print("Motion Data Info:")
print(motion_df.info())

print("\nTemperature Data Info:")
print(temperature_df.info())

# Summary statistics for numerical columns
print("\nMotion Data Summary:")
print(motion_df.describe())

print("\nTemperature Data Summary:")
print(temperature_df.describe())

# Extract additional features from the timestamp
motion_df['hour'] = motion_df['motion_timestamp'].dt.hour
motion_df['day_of_week'] = motion_df['motion_timestamp'].dt.dayofweek
temperature_df['hour'] = temperature_df['temp_timestamp'].dt.hour
temperature_df['day_of_week'] = temperature_df['temp_timestamp'].dt.dayofweek

# Motion count by hour and day of week
motion_by_hour = motion_df.groupby('hour').size()
motion_by_day = motion_df.groupby('day_of_week').size()

# Temperature count by hour and day of week
temperature_by_hour = temperature_df.groupby('hour')['temp_value'].mean()
temperature_by_day = temperature_df.groupby('day_of_week')['temp_value'].mean()

# Plotting the results
plt.figure(figsize=(12, 6))

# Plot motion data by hour
plt.subplot(2, 2, 1)
sns.lineplot(x=motion_by_hour.index, y=motion_by_hour.values)
plt.title('Motion Count by Hour')
plt.xlabel('Hour of the Day')
plt.ylabel('Motion Count')

# Plot temperature data by hour
plt.subplot(2, 2, 2)
sns.lineplot(x=temperature_by_hour.index, y=temperature_by_hour.values)
plt.title('Average Temperature by Hour')
plt.xlabel('Hour of the Day')
plt.ylabel('Temperature')

# Plot motion data by day of week
plt.subplot(2, 2, 3)
sns.lineplot(x=motion_by_day.index, y=motion_by_day.values)
plt.title('Motion Count by Day of Week')
plt.xlabel('Day of Week')
plt.ylabel('Motion Count')

# Plot temperature data by day of week
plt.subplot(2, 2, 4)
sns.lineplot(x=temperature_by_day.index, y=temperature_by_day.values)
plt.title('Average Temperature by Day of Week')
plt.xlabel('Day of Week')
plt.ylabel('Temperature')

plt.tight_layout()
plt.show()

# Plot histogram of temperature distribution
plt.figure(figsize=(8, 6))
sns.histplot(temperature_df['temp_value'], kde=True, color='blue', bins=30)
plt.title('Temperature Value Distribution')
plt.xlabel('Temperature (°C)')
plt.ylabel('Frequency')

# Add a vertical line for mean and median
mean_temp = temperature_df['temp_value'].mean()
median_temp = temperature_df['temp_value'].median()
plt.axvline(mean_temp, color='red', linestyle='--', label=f'Mean ({mean_temp:.2f}°C)')
plt.axvline(median_temp, color='green', linestyle='--', label=f'Median ({median_temp:.2f}°C)')

plt.legend()
plt.show()

# Box plot to detect outliers in temperature data
plt.figure(figsize=(8, 6))
sns.boxplot(x=temperature_df['temp_value'], color='lightblue')
plt.title('Box Plot of Temperature Values')
plt.xlabel('Temperature (°C)')

# Highlight outliers with a different color
sns.boxplot(x=temperature_df['temp_value'], color='lightblue', fliersize=5, flierprops=dict(markerfacecolor='red', marker='o'))
plt.show()

# Filter values greater than a threshold for dangerous temperatures
threshold_temp = 70
dangerous_temps = temperature_df[temperature_df['temp_value'] > threshold_temp]

print(f"Dangerous Temperatures (Above {threshold_temp}°C):")
print(dangerous_temps)
