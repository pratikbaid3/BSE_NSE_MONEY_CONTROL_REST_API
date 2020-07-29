import sqlite3
from datetime import datetime

def latest_ca(request):
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    if start_date:
        start_date = datetime.strptime(start_date, "%d-%b-%Y").strftime("%Y-%m-%d")
    if end_date:
        end_date = datetime.strptime(end_date, "%d-%b-%Y").strftime("%Y-%m-%d")
    company_name = request.args.get('company_name', '')
    conn = sqlite3.connect('corporate_action.db')
    c = conn.cursor()
    query =""
    if start_date and end_date:
        query = f'SELECT * FROM latest_mc_ca WHERE company_name LIKE "%{company_name}%" AND ex_date BETWEEN date("{start_date}") and date("{end_date}")'
    elif start_date:
        query = f'SELECT * FROM latest_mc_ca WHERE company_name LIKE "%{company_name}%" AND ex_date >= date("{start_date}")'
    elif end_date:
        query = f'SELECT * FROM latest_mc_ca WHERE company_name LIKE "%{company_name}%" AND ex_date <= date("{end_date}")'
    else:
        query = f'SELECT * FROM latest_mc_ca WHERE company_name LIKE "%{company_name}%"'
    print(query)
    c.execute(query)
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