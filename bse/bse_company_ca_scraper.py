import requests
import json
from bs4 import BeautifulSoup as soup
import os
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

def company_ca_scraper(security_name,security_code):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    # options = webdriver.ChromeOptions()
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--incognito')
    # options.add_argument("--headless")
    # driver = webdriver.Chrome("/Users/pratikbaid/Developer/chromedriver", chrome_options=options)

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
    return(ca_array)

print(company_ca_scraper('BOMDYEING','500020'))