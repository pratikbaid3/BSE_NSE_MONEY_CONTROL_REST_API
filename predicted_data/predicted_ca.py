import sqlite3

def latest_ca():
    conn=sqlite3.connect('corporate_action.db')
    c=conn.cursor()
    c.execute('SELECT * FROM predicted_ca')
    ca_array=[]
    for data in c:
        security_name=data[0]
        purpose=data[1]
        date=data[2]
        content=data[3]
        if(data[1]=='' ):
            purpose='-'
        if(data[2]=='' ):
            date='-'
    
        corporate_action={
            'security_name':security_name,
            'purpose':purpose,
            'date':date,
            'content':content,
        }
        ca_array.append(corporate_action)
    conn.commit()
    conn.close()
    return (ca_array)