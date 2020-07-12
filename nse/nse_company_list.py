import requests
from bs4 import BeautifulSoup as bs4
import pandas as pd
import os
import warnings

def get_csv_link():
    NSE_COMPANY_LIST_URL = "https://www.nseindia.com/regulations/listing-compliance/nse-market-capitalisation-all-companies"
    res = requests.get(
        NSE_COMPANY_LIST_URL,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        },
    )
    res.raise_for_status()

    soup = bs4(res.content, features='lxml')
    divHolders=soup.find_all('div',{"class":"mt-3"})
    for div in divHolders:
        if div.find('a', {"data-entity-type": "file"}):
            element = div.find('a', {"data-entity-type": "file"})
            return element['href']

def get_company_list():
    url = get_csv_link()
    if not url:
        return []
    res = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        },
    )
    res.raise_for_status()
    with open("nse_company_list.xlsx",'wb') as f:
        f.write(res.content)
    xlsx_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'nse_company_list.xlsx')
    if not os.path.exists(xlsx_path):
        warnings.warn("Cannot download file from NSE")
        return []
    df = pd.read_excel(xlsx_path)
    df = df[['Symbol', 'Company Name']]
    df = df.dropna()
    data = df.T.to_dict().values()
    return data

company_list = get_company_list()