import requests
import json
from bs4 import BeautifulSoup as soup
import os
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import sqlite3
import time

def company_ca_scraper(security_name,security_code):
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--no-sandbox")
    # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument("--headless")
    driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", options=options)

    driver.get('https://www.bseindia.com/corporates/corporate_act.aspx')
    name_xpath = '//*[@id="ContentPlaceHolder1_SmartSearch_smartSearch"]'
    submit_xpath = '//*[@id="ContentPlaceHolder1_btnSubmit"]'
    driver.find_element_by_xpath(name_xpath).send_keys(security_name)
    arg1_xpath = '//*[@id="ContentPlaceHolder1_SmartSearch_hdnCode"]'
    arg2_xpath = '//*[@id="ContentPlaceHolder1_hf_scripcode"]'
    arg1 = driver.find_element_by_xpath(arg1_xpath)
    arg2 = driver.find_element_by_xpath(arg2_xpath)
    driver.execute_script(f'arguments[0].value = "{security_code}"', arg1)
    driver.execute_script(f'arguments[0].value = "{security_code}"', arg2)
    driver.find_element_by_xpath(submit_xpath).click()

    pageSource=driver.page_source
    page_soup = soup(pageSource,features='lxml')
    no_of_pages_tab=page_soup.find('tr',{'class':'pgr'})
    if(no_of_pages_tab==None):
        no_of_pages=1
    else:
        no_of_pages=len(no_of_pages_tab.find_all('a'))+1

    dataList=[]

    if(no_of_pages == 1):
        pageSource=driver.page_source
        page_soup = soup(pageSource,features='lxml')
        dataRows=page_soup.find_all('tr',{"class":"TTRow"})
        for dataRow in dataRows:
            dataColumns=dataRow.find_all('td')
            data=[]
            for dataColumn in dataColumns:
                data.append(dataColumn.text)
            dataList.append(data)

    elif(no_of_pages>1):

        pageSource=driver.page_source
        page_soup = soup(pageSource,features='lxml')
        dataRows=page_soup.find_all('tr',{"class":"TTRow"})
        for dataRow in dataRows:
            dataColumns=dataRow.find_all('td')
            data=[]
            for dataColumn in dataColumns:
                data.append(dataColumn.text)
            dataList.append(data)

        for i in range (2,no_of_pages+1):
            xpath=f'//*[@id="ContentPlaceHolder1_gvData"]/tbody/tr[1]/td/table/tbody/tr/td[{i}]/a'
            print("\n"+ xpath + "\n")
            WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath(xpath))
            driver.find_element_by_xpath(xpath).click()
            print()
            print("Entered ",i)
            print()
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
    return(dataList)


#Initializing the database
conn=sqlite3.connect('corporate_action.db')
c=conn.cursor()
c_new=conn.cursor()
create_table="CREATE TABLE IF NOT EXISTS bse_ca (key text PRIMARY KEY UNIQUE,security_code text, security_name text, ex_date text, purpose text, record_date text,bc_start_date text,bc_end_date text,nd_start_date text,nd_end_date text,actual_payment_date text)"
c.execute(create_table)
create_table="CREATE TABLE IF NOT EXISTS not_scraped(code text,company text)"
c.execute(create_table)

c_new.execute('SELECT * FROM bse_companies')
company_list=[]
for comp in c_new:
    company_list.append(comp)
list_len=len(company_list)
for i in range(3323,list_len):
    # Adding data to the database
    company=company_list[i]
    dataList=company_ca_scraper(company[1],company[0])
    #print(dataList)
    add_data_to_db="INSERT INTO bse_ca VALUES (?,?,?,?,?,?,?,?,?,?,?)"
    companies_not_scraped='INSERT INTO not_scraped VALUES(?,?)'
    print(f'#${i}')
    print(f'Scraping ${company[1]}')
    if(len(dataList)==0):
        print('NO DATA')
        c.execute(companies_not_scraped,(company[0],company[1]))
    else:
        print('DATA')
        for data in dataList:
            uniqueKey=data[0]+data[2]+data[3]
            try:
                c.execute(add_data_to_db,(uniqueKey,data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9]))
            except:
                print('Skipped')
    conn.commit()
    # if(i%4==0):
    #     print('SLEEPING')
    #     time.sleep(180)
    #     print('SLEEP OVER')
    print()

conn.close()
print ('Corporate Action Added Successfully')
