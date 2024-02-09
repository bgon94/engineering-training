import requests
import pandas as pd
from io import StringIO
import psycopg2
from sqlalchemy import create_engine
from tabulate import tabulate
import os
import shutil

#Downloads csv from website, renames the file and moves into working directory:

file_url = 'https://nflsavant.com/pbp_data.php?year=2023'
destination_directory = r'C:\Users\bgoncalves\Desktop\Engineering Test Projects\Loading data with python'
response = requests.get(file_url)

if response.status_code == 200:
   
   file_name = 'pbp-2023.csv'
   with open(file_name, 'wb') as file:
      file.write(response.content)

   shutil.move(file_name, os.path.join(destination_directory, file_name))

#Puts csv into a df:

file_path = 'pbp-2023.csv'
df = pd.read_csv(file_path)

#filters out NY Giants vs GB Packers game 12/1/23

filtered_df = df[df['GameId'] == 2023121101]
sorted_df = filtered_df.sort_values(by=['Quarter'])

print(sorted_df)

db_config = {
    'user': 'postgres',
    'password': 'Bb!!14789632',
    'host': 'localhost',
    'port': '5432',
    'database': 'postgres'
}

#creates connection to DB
engine = create_engine(f'postgresql+psycopg2://{db_config["user"]}:{db_config["password"]}@{db_config["host"]}:{db_config["port"]}/{db_config["database"]}')
table_name = 'pbp'

#insert statement
filtered_df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)

