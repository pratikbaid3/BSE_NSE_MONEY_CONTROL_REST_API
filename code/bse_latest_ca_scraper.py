import requests
import json
from bs4 import BeautifulSoup as soup
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
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless') #This prevents the browser from opening up
        driver = webdriver.Chrome("/Users/pratikbaid/Developer/chromedriver", chrome_options=options)

    pageSource=res.content
    dataList=[]
    page_soup = soup(pageSource,features='lxml')
    dataRows=page_soup.find_all('tr',{"class":"TTRow"})
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
            
        

    ca_array=[]
    conn=sqlite3.connect('corporate_action.db')
    c=conn.cursor()
    create_table="CREATE TABLE IF NOT EXISTS latest_bse_ca (security_code text, security_name text, ex_date text, purpose text, record_date text,bc_start_date text,bc_end_date text,nd_start_date text,nd_end_date text,actual_payment_date text)"
    c.execute(create_table)
    add_data_to_db="INSERT INTO latest_bse_ca VALUES (?,?,?,?,?,?,?,?,?,?)"
    for data in dataList:
        c.execute(add_data_to_db,(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9]))
        corporate_action={
            'security_code':data[0],
            'security_name':data[1],
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
    conn.commit()
    conn.close()
    return (ca_array)