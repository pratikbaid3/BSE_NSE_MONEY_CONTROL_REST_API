import requests
import json
from bs4 import BeautifulSoup as soup
from selenium import webdriver

def latest_ca_scrape():
    res = requests.get('https://www.bseindia.com/corporates/corporate_act.aspx')
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
    return (ca_array)