import sqlite3

def company_ca(security_code):
    conn=sqlite3.connect('corporate_action.db')
    c=conn.cursor()
    c.execute(f'SELECT * FROM bse_ca WHERE security_code = {security_code}')
    ca_array=[]
    for data in c:
        corporate_action={
            'security_code':data[1],
            'security_name':data[2],
            'ex_date':data[3],
            'purpose':data[4],
            'record_date':data[5],
            'bc_start_date':data[6],
            'bc_end_date':data[7],
            'nd_start_date':data[8],
            'nd_end_date':data[9],
            'actual_payment_date':data[10]
        }
        ca_array.append(corporate_action)
    conn.commit()
    conn.close()
    return (ca_array)