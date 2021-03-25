import pandas as pd
from sqlalchemy import create_engine
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

Config = {
    'db_user': 'username',
    'db_pass': 'password',
    'db_host': 'postgres_container',
    'db_port': '5432',
    'db_name': 'postgres'
}


# --- #

db_user = Config['db_user']
db_pass = Config['db_pass']
db_host = Config['db_host']
db_port = Config['db_port']
db_name = Config['db_name']

netflix_df = pd.read_csv("netflix_data.csv", index_col="show_id")

# We don't need all columns.
netflix_df_small = netflix_df[
    [
        "type", 
        "title", 
        "country", 
        "date_added", 
        "release_year", 
        "rating", 
        "duration"
    ]
]

# Create the connection to the database, then store the dataframe in the table "netflix_data"
engine = create_engine(f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}')
netflix_df_small.to_sql("netflix_data", engine, if_exists='replace', index=False)

# --- #

