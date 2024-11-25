from sqlalchemy import create_engine

# Database connection parameters
host = '10.134.178.157'
port = 5432
database = 'postgres'
user = 'team7'
password = 'team7password!'

# Create the connection string dynamically
connection_string = f'postgresql://{user}:{password}@{host}:{port}/{database}'

# Connect to your database
engine = create_engine(connection_string)

# Test the connection
try:
    with engine.connect() as connection:
        print("Database connection successful!")
except Exception as e:
    print(f"Error connecting to the database: {e}")
