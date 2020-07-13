import sqlite3

def company_ca(symbol):
    conn=sqlite3.connect('corporate_action.db')
    c=conn.cursor()

    sym=symbol.strip()

    c.execute('SELECT * FROM mc_ca WHERE company_name = ?',(symbol,))
    ca_array=[]
    for data in c:
        corporate_action={
            'company_name':data[1],
            'purpose':data[2],
            'anouncement':data[3],
            'record_date':data[4],
            'ex-date':data[5],
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