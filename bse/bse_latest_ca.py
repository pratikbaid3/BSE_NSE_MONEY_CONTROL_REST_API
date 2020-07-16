import sqlite3

def latest_ca():
    conn=sqlite3.connect('corporate_action.db')
    c=conn.cursor()
    c.execute('SELECT * FROM latest_bse_ca')
    ca_array=[]
    for data in c:
        security_name=data[2][1:len(data[2])-1]
        if(data[10]=='\n-\n' ):
            actual_payment_data='-'
        else:
            actual_payment_data=data[10]
    
        corporate_action={
            'security_code':data[1],
            'security_name':security_name,
            'ex_date':data[3],
            'purpose':data[4],
            'record_date':data[5],
            'bc_start_date':data[6],
            'bc_end_date':data[7],
            'nd_start_date':data[8],
            'nd_end_date':data[9],
            'actual_payment_date':actual_payment_data
        }
        ca_array.append(corporate_action)
    conn.commit()
    conn.close()
    return (ca_array)