import requests
import json
from bs4 import BeautifulSoup as soup
import os
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import sqlite3

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
    driver.execute_script(f"arguments[0].value = '{security_code}'", arg1)
    driver.execute_script(f"arguments[0].value = '{security_code}'", arg2)
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
    # for data in dataList:
    #     corporate_action={
    #         'secuarity_code':data[0],
    #         'secuarity_name':data[1],
    #         'ex_date':data[2],
    #         'purpose':data[3],
    #         'record_date':data[4],
    #         'bc_start_date':data[5],
    #         'bc_end_date':data[6],
    #         'nd_start_date':data[7],
    #         'nd_end_date':data[8],
    #         'actual_payment_date':data[9]
    #     }
    #     ca_array.append(corporate_action)
    return(dataList)


#Initializing the database
conn=sqlite3.connect('corporate_action.db')
c=conn.cursor()
c_new=conn.cursor()
create_table="CREATE TABLE IF NOT EXISTS bse_ca (key text PRIMARY KEY UNIQUE,security_code text, security_name text, ex_date text, purpose text, record_date text,bc_start_date text,bc_end_date text,nd_start_date text,nd_end_date text,actual_payment_date text)"
c.execute(create_table)

#Adding data to the database
dataList=company_ca_scraper('BOMDYEING','500020')
add_data_to_db="INSERT INTO bse_ca VALUES (?,?,?,?,?,?,?,?,?,?,?)"
for data in dataList:
    uniqueKey=data[0]+data[2]+data[3]
    c.execute(add_data_to_db,(uniqueKey,data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9]))
conn.commit()
conn.close()
print ('latest corporate action database updated successfully')
