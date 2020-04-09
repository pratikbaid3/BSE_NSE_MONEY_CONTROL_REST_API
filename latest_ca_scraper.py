import requests
import json
from bs4 import BeautifulSoup as soup

def latest_ca_scrape():
    res = requests.get('https://www.bseindia.com/corporates/corporate_act.aspx')
    res.raise_for_status()
    page_soup = soup(res.content,features='lxml')

    dataRows=page_soup.find_all('tr',{"class":"TTRow"})
    dataList=[]
    for dataRow in dataRows:
        dataColumns=dataRow.find_all('td')
        data=[]
        for dataColumn in dataColumns:
            data.append(dataColumn.text)
        dataList.append(data)

    ca_array=[]
    for data in dataList:
        corporate_action={
            'secuarity_code':data[0],
            'secuarity_name':data[1],
            'ex_date':data[2],
            'purpose':data[3],
            'record_date':data[4],
            'bc_start_date':data[5],
            'bc_end_date':data[6],
            'nd_start_date':data[7],
            'nd_end_date':data[8],
            'actual_payment_date':data[9]
        }
        ca_array.append(corporate_action)
    latest_ca_json={
        'Latest_CA':ca_array
    }
    json_data=json.dumps(latest_ca_json)
    return(json_data)