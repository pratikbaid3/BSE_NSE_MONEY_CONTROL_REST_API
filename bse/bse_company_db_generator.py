import json
import sqlite3

with open('./stk.json') as f:
    data=json.load(f)

conn=sqlite3.connect('corporate_action.db')
c=conn.cursor()
c_new=conn.cursor()
create_table="CREATE TABLE IF NOT EXISTS bse_companies (code text PRIMARY KEY UNIQUE,company text)"
c.execute(create_table)
add_data_to_db="INSERT INTO bse_companies VALUES (?,?)"

for (i,j) in data.items():
    c.execute(add_data_to_db,(i,j))

conn.commit()
conn.close()
