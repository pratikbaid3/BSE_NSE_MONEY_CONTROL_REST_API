import sqlite3

def latest_ca():
    conn=sqlite3.connect('corporate_action.db')
    c=conn.cursor()
    c.execute('SELECT * FROM predicted_ca')
    ca_array=[]
    for data in c:
        security_name=data[0]
        category=data[1]
        purpose=data[2]
        date=data[3]
        content=data[4]
        if(data[1]=='' ):
            purpose='-'
        if(data[2]=='' ):
            date='-'
    
        corporate_action={
            'security_name':security_name,
            'category':category,
            'purpose':purpose,
            'date':date,
            'content':content,
        }
        ca_array.append(corporate_action)
    conn.commit()
    conn.close()
    return (ca_array)