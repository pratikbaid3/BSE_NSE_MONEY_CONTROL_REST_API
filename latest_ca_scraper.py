import requests
import json
from bs4 import BeautifulSoup as soup

def latest_ca_scrape():
    res = requests.get('https://www.bseindia.com/corporates/corporate_act.aspx')
    res.raise_for_status()
    page_soup = soup(res.content,features='lxml')
    nameAndPurpose=page_soup.find_all('td',{"class":"TTRow_left"})
    secuarityCode=page_soup.find_all('a',{"class":"tablebluelink"})
    noOfCorporateActions=len(nameAndPurpose)
    i=0
    j=0
    ca_array=[]
    while (i<noOfCorporateActions):
        coorporate_action={
            'secuarity_code':secuarityCode[j].text,
            'secuarity_name':nameAndPurpose[i].text,
            'purpose':nameAndPurpose[i+1].text
        }
        ca_array.append(coorporate_action)
        i=i+2
    latest_ca_json={
        'Latest_CA':ca_array
    }
    json_data=json.dumps(latest_ca_json)
    return(json_data)