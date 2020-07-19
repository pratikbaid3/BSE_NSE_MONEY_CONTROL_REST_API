import json
import sqlite3

with open('./stk.json') as f:
    data=json.load(f)

conn=sqlite3.connect('companies.db')
c=conn.cursor()
c_new=conn.cursor()
create_table="CREATE TABLE IF NOT EXISTS companies (exchange text,code text,company text)"
c.execute(create_table)
add_data_to_db="INSERT INTO companies VALUES (?,?,?)"

for (i,j) in data.items():
    c.execute(add_data_to_db,('BSE',i,j))

conn.commit()
conn.close()
