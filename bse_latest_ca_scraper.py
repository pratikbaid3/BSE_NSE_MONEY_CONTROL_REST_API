import requests
import json
from bs4 import BeautifulSoup as soup
import os
from selenium import webdriver
import sqlite3

def latest_ca_scrape():
    res = requests.get('https://www.bseindia.com/corporates/corporate_act.aspx',headers={'User-Agent':'Mozilla/5.0'})
    res.raise_for_status()
    page_soup = soup(res.content,features='lxml')

    no_of_pages_tab=page_soup.find('tr',{'class':'pgr'})
    if(no_of_pages_tab==None):
        no_of_pages=1
    else:
        no_of_pages=len(no_of_pages_tab.find_all('a'))+1
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        # options = webdriver.ChromeOptions()
        # options.add_argument('--ignore-certificate-errors')
        # options.add_argument('--incognito')
        # options.add_argument('--headless') #This prevents the browser from opening up
        # driver = webdriver.Chrome("/Users/pratikbaid/Developer/chromedriver", chrome_options=options)

    pageSource=res.content
    dataList=[]
    page_soup = soup(pageSource,features='lxml')
    dataRows=page_soup.find_all('tr',{"class":"TTRow"})

    #Scraping the data and adding it into the dataList
    for dataRow in dataRows:
        dataColumns=dataRow.find_all('td')
        data=[]
        for dataColumn in dataColumns:
            data.append(dataColumn.text)
        dataList.append(data)

    if(no_of_pages>1):
        print('Entered first if')

        for i in range (2,no_of_pages+1):
            print("Entered ",i)
            xpath=f'//*[@id="ContentPlaceHolder1_gvData"]/tbody/tr[1]/td/table/tbody/tr/td[{i}]/a'
            print(xpath)
            driver.get('https://www.bseindia.com/corporates/corporate_act.aspx')
            driver.find_element_by_xpath(xpath).click()
            pageSource=driver.page_source
            page_soup = soup(pageSource,features='lxml')
            dataRows=page_soup.find_all('tr',{"class":"TTRow"})
            for dataRow in dataRows:
                dataColumns=dataRow.find_all('td')
                data=[]
                for dataColumn in dataColumns:
                    data.append(dataColumn.text)
                dataList.append(data)
            
    #Initializing the database
    conn=sqlite3.connect('corporate_action.db')
    c=conn.cursor()
    c_new=conn.cursor()
    create_table="CREATE TABLE IF NOT EXISTS latest_bse_ca (key text PRIMARY KEY UNIQUE,security_code text, security_name text, ex_date text, purpose text, record_date text,bc_start_date text,bc_end_date text,nd_start_date text,nd_end_date text,actual_payment_date text)"
    c.execute(create_table)

    #Transfering the data of the latest corporate action to the storage
    create_table="CREATE TABLE IF NOT EXISTS bse_ca (key text PRIMARY KEY UNIQUE,security_code text, security_name text, ex_date text, purpose text, record_date text,bc_start_date text,bc_end_date text,nd_start_date text,nd_end_date text,actual_payment_date text)"
    c_new.execute(create_table)
    c_new.execute('SELECT * FROM latest_bse_ca')
    add_data_to_db="INSERT INTO bse_ca VALUES (?,?,?,?,?,?,?,?,?,?,?)"
    for data in c_new:
        try:
            c.execute(add_data_to_db,(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10]))
        except:
            print('Skipped')
    #Deleting the preexisting data from the database
    c.execute('DELETE FROM latest_bse_ca')

    #Adding data to the database
    add_data_to_db="INSERT INTO latest_bse_ca VALUES (?,?,?,?,?,?,?,?,?,?,?)"
    for data in dataList:
        uniqueKey=data[0]+data[2]+data[3]
        c.execute(add_data_to_db,(uniqueKey,data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9]))
    conn.commit()
    conn.close()
    return ('latest corporate action database updated successfully')