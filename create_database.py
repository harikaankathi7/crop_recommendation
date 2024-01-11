import sqlite3
conn=sqlite3.connect('cropdata.db')
cur=conn.cursor()
cur.execute('CREATE TABLE CROPS(N FLOAT, P FLOAT,K FLOAT,TEMPERATURE FLOAT,HUMIDITY FLOAT,PH FLOAT,RAINFALL FLOAT,PREDICTED_CROP VARCHAR(30))')
conn.commit()