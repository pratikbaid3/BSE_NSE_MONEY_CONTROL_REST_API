import requests
import json
from selenium import webdriver
from bs4 import BeautifulSoup as bs4
import sqlite3

class NSEScraper():
    def __init__(self):
        self.NSE_CORPORATE_ACTION_HOMEPAGE_URL = "https://www1.nseindia.com/sme/marketinfo/corporates/actions/latestCorpActions.jsp?currentPage={}"
        self.soup = None
        self.data = []
        self.data_format = [
            'Symbol',
            'Company Name',
            'Series',
            'Face Value',
            'Purpose',
            'Ex-Date',
            'Record Date',
            'BC Start-Date',
            'BC End-Date'
        ]
        self.page = 1

    def __str__(self):
        return "NSE Scraper"

    def __repr__(self):
        return "NSE Scraper()"
    
    def get_data(self):
        return self.data

    def add_soup(self):
        res = requests.get(self.NSE_CORPORATE_ACTION_HOMEPAGE_URL.format(self.page), headers={
                           'User-Agent': 'Mozilla/5.0'})
        status = res.status_code
        if status == 200:
            self.soup = bs4(res.content, features='lxml')

    def print_soup(self):
        if __name__ == "__main__":
            print(self.get_soup())

    def setup(self):
        self.add_soup()

    def get_data_text(self, element):
        not_present = ['-']
        if element is None:
            return None
        text = element.getText()
        if text in not_present:
            return None
        return text.strip()

    def scrape_data(self):
        self.setup()
        table = self.soup.find_all('table')[1]
        scraped_corporate_datas = table.find_all('tr')
        if len(scraped_corporate_datas) <= 1:
            return False
        for corporate_data in scraped_corporate_datas:
            scraped_data = corporate_data.find_all('td')
            if len(scraped_data) <= 0:
                continue
            temp_data = {}
            for index, data in enumerate(scraped_data):
                # Two extra columns are present, ND Start Date and ND End Date which is null
                if index < len(self.data_format):
                    textual_data = self.get_data_text(data)
                    temp_data[self.data_format[index]] = textual_data
            self.data.append(temp_data)
        return True
    
    def get_all_corporate_actions(self):
        status = self.scrape_data()
        if status:
            self.page += 1
            self.get_all_corporate_actions()


    def display_data(self):
        if __name__ == "__main__":
            print(self.get_data())
#Initializing the scraper
nse=NSEScraper()
nse.get_all_corporate_actions()
nse_data_list=nse.get_data()

#Initializing DB
conn=sqlite3.connect('corporate_action.db')
c=conn.cursor()
c_new=conn.cursor()
create_table="CREATE TABLE IF NOT EXISTS latest_nse_ca (key text PRIMARY KEY UNIQUE,symbol text, company_name text, series text, face_value text, purpose text,ex_date text,record_date text,bc_start_date text,bc_end_date text)"
c.execute(create_table)

#Transfering the data of the latest corporate action to the storage
create_table="CREATE TABLE IF NOT EXISTS nse_ca (key text PRIMARY KEY UNIQUE,symbol text, company_name text, series text, face_value text, purpose text,ex_date text,record_date text,bc_start_date text,bc_end_date text)"
c_new.execute(create_table)
c_new.execute('SELECT * FROM latest_nse_ca')
add_data_to_db="INSERT INTO nse_ca VALUES (?,?,?,?,?,?,?,?,?,?)"
for data in c_new:
    try:
        c.execute(add_data_to_db,(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9]))
    except:
        print('Skipped')
#Deleting the pre-existing data from the database
c.execute('DELETE FROM latest_nse_ca')


#Refreshing the latest ca db
add_data_to_db="INSERT INTO latest_nse_ca VALUES (?,?,?,?,?,?,?,?,?,?)"

for nse_data in nse_data_list:
    if(nse_data['Ex-Date']!=None):
        key=nse_data['Symbol']+nse_data['Purpose']+nse_data['Ex-Date']
        try:
            c.execute(add_data_to_db,(key,nse_data['Symbol'],nse_data['Company Name'],nse_data['Series'],nse_data['Face Value'],nse_data['Purpose'],nse_data['Ex-Date'],nse_data['Record Date'],nse_data['BC Start-Date'],nse_data['BC End-Date']))
        except:
            print(nse_data)
    else:
        print(nse_data)
conn.commit()
conn.close()

print('Scraped Data Successfully')
