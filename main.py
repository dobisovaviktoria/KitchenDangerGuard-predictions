import pandas as pd
from sqlalchemy import create_engine
# Connect to your database
engine = create_engine('postgresql://team7:team7password!@10.134.178.157/postgres')

# Load motion and temperature data
motion_df = pd.read_sql('SELECT * FROM motion_data', engine)
temperature_df = pd.read_sql('SELECT * FROM temperature_data', engine)

print(motion_df)