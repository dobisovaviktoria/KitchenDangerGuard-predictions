import pandas as pd
from sqlalchemy import create_engine, text

# Example database connection (replace with your actual database connection string)
DB_CONFIG = {
    "host": "10.134.178.157",
    "user": "team7",
    "password": "team7password!",
    "dbname": "postgres"
}

# Establish database connection
def get_engine():
    conn_string = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['dbname']}"
    return create_engine(conn_string)

def fetch_all_devices():
    # Create an engine instance
    engine = get_engine()

    # Connect to the database and execute the query
    with engine.connect() as connection:
        # Define your query to fetch all devices (adjust this query as needed)
        query = text("SELECT distinct arduino_device_id FROM sensor_data")  # Wrap the query in `text()`

        # Execute the query and fetch all results
        result = connection.execute(query).fetchall()

    # Return the device IDs from the result
    return [row[0] for row in result]  # Assuming device_id is the first column


# Fetch data for a specific Arduino device
def fetch_data(arduino_id):
    engine = get_engine()
    query = f"""
    SELECT timestamp, temperature_value, motion_status
    FROM sensor_data
    WHERE arduino_device_id = '{arduino_id}'
    ORDER BY timestamp;
    """
    data = pd.read_sql(query, engine)

    # Convert 'timestamp' to datetime, with 'coerce' to handle invalid formats
    data['timestamp'] = pd.to_datetime(data['timestamp'], errors='coerce')

    # Check if there are any invalid timestamps (NaT) after conversion
    if data['timestamp'].isnull().any():
        print("Warning: There are invalid timestamps in the data.")

    return data

