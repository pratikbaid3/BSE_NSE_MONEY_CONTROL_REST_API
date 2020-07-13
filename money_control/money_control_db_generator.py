import requests
import json
import re
from bs4 import BeautifulSoup as soup
import sqlite3

def money_control_get_company_names():
    conn=sqlite3.connect('corporate_action.db')
    c=conn.cursor()
    data = []
    res = requests.get('https://www.moneycontrol.com/india/stockpricequote/',headers={'User-Agent':'Mozilla/5.0'})
    res.raise_for_status()
    page_soup = soup(res.content,features='lxml')
    links=page_soup.find_all('a',{'class':'bl_12'})
    for link in links[1:]:
        data.append({
            'name': link.string,
            'link': link['href'],
            'bse': money_control_get_company_bse(link['href'])
        })
        print(money_control_get_company_bse(link['href']))
        print(link.string)
        print()
        #Adding data to db
        add_data_to_db="INSERT INTO mc_companies VALUES (?,?)"
        c.execute(add_data_to_db,(money_control_get_company_bse(link['href']),link.string))
        conn.commit()

    print('Completed Scraping')

def money_control_get_company_bse(link):
	res = requests.get(link,headers={'User-Agent':'Mozilla/5.0'})
	res.raise_for_status()
	page_soup = soup(res.content,features='lxml')
	bse = page_soup.find_all('ctag',{'class':'mob-hide'})[0].find_all('span')[0].string
	return bse

#Initializing the db
conn=sqlite3.connect('corporate_action.db')
c=conn.cursor()
c_new=conn.cursor()
create_table="CREATE TABLE IF NOT EXISTS mc_companies (code text PRIMARY KEY UNIQUE,company text)"
c.execute(create_table)
money_control_get_company_names()
conn.commit()
conn.close()