import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import psycopg2
import pandas.io.sql as psql


print('Attempting to connect to database')
conn = psycopg2.connect("dbname='fuser' user='fuser' password='fuser' host='localhost' ")
conn_tack = psycopg2.connect("dbname='fuser' user='fuser' password='fuser' host='localhost' port='54321' ")
#conn = psycopg2.connect("dbname='fuserclt' user='fuserclt' password='fuserclt' host='localhost' ")


q = '''SELECT 
*
FROM
matm_flight_all
where timestamp > '2018-11-09 00:00:00'
and release_requested_roll_time is not null
ORDER BY
timestamp DESC
LIMIT 100
'''
df = psql.read_sql(q, conn)

df.to_csv('test.csv')

flight_list = df['gufi'].unique()

for flight in range(len(flight_list)):
	df_temp = df[ df['gufi'] == flight_list[flight] ].reset_index(drop=True)
	#df_temp = df_temp.