import sqlite3
from datetime import datetime

def latest_ca(request):
    c = conn.cursor()
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    if start_date:
        start_date = datetime.strptime(start_date, "%d-%b-%Y").strftime("%Y-%m-%d")
    if end_date:
        end_date = datetime.strptime(end_date, "%d-%b-%Y").strftime("%Y-%m-%d")
    security_name = request.args.get('company_name', '')
    conn = sqlite3.connect('corporate_action.db')
    c = conn.cursor()
    query =""
    if start_date and end_date:
        query = f'SELECT * FROM latest_bse_ca WHERE security_name LIKE "%{security_name}%" AND ex_date BETWEEN date("{start_date}") and date("{end_date}")'
    elif start_date:
        query = f'SELECT * FROM latest_bse_ca WHERE security_name LIKE "%{security_name}%" AND ex_date >= date("{start_date}")'
    elif end_date:
        query = f'SELECT * FROM latest_bse_ca WHERE security_name LIKE "%{security_name}%" AND ex_date <= date("{end_date}")'
    else:
        query = f'SELECT * FROM latest_bse_ca WHERE security_name LIKE "%{security_name}%"'
    print(query)
    c.execute(query)
    ca_array = []
    for data in c:
        security_name = data[2][1:len(data[2])-1]
        if(data[10] == '\n-\n'):
            actual_payment_data = '-'
        else:
            actual_payment_data = data[10]

        corporate_action = {
            'security_code': data[1],
            'security_name': security_name,
            'ex_date': datetime.strptime(data[3], "%Y-%m-%d").strftime("%d-%b-%Y"),
            'purpose': data[4],
            'record_date': data[5],
            'bc_start_date': data[6],
            'bc_end_date': data[7],
            'nd_start_date': data[8],
            'nd_end_date': data[9],
            'actual_payment_date': actual_payment_data
        }
        ca_array.append(corporate_action)
    conn.commit()
    conn.close()
    return (ca_array)
