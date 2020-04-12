import json
import requests
from bs4 import BeautifulSoup as soup


def companyDataScraper(secuarity_code,secuarity_name):
    url='https://www.bseindia.com/corporates/corporate_act.aspx?scripcode='+secuarity_code+'&scripname='+secuarity_name
    print(url)
    res=requests.get(url)
    res.raise_for_status()
    page_soup=soup(res.content,features='lxml')


    no_of_pages_tab=page_soup.find('tr',{'class':'pgr'})
    no_of_pages=len(no_of_pages_tab.find_all('a'))+1

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

    company_ca_json={
        'CA of '+secuarity_name :ca_array
    }
    json_data=json.dumps(company_ca_json)
    print(no_of_pages)
    return(json_data)