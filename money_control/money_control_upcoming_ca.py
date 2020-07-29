import sqlite3
from datetime import datetime

def latest_ca():
    conn=sqlite3.connect('corporate_action.db')
    c=conn.cursor()
    c.execute('SELECT * FROM latest_mc_ca')
    ca_array=[]
    for data in c:
        corporate_action={
            'company_name':data[1],
            'purpose':data[2],
            'anouncement':data[3],
            'record_date':data[4],
            'ex-date':datetime.strptime(data[5], "%Y-%m-%d").strftime("%d-%b-%Y"),
            'bc_start_date':'None',
            'bc_end_date':'None',
            'nd_start_date':'None',
            'nd_end_date':'None',
            'actual_payment_date':'None'
        }
        ca_array.append(corporate_action)
    conn.commit()
    conn.close()
    return (ca_array)