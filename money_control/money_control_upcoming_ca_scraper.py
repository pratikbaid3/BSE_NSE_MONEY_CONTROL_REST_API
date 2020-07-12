import requests
import json
from bs4 import BeautifulSoup as soup

def money_control_ca_scraper():

    ca_list=[]

    res=requests.get('https://www.moneycontrol.com/stocks/marketinfo/upcoming_actions/home.html')
    res.raise_for_status()
    page_soup=soup(res.content,features='lxml')

    div=page_soup.find_all('div',{'class':'tbldata36 PT20'})
    bonus_div=page_soup.find('div',{'class':'tbldata36 PT10'})
    splits_div=div[0]
    rights_div=div[1]
    dividends_div=div[2]

    def check_if_div_empty(temp_div):
        td=temp_div.find_all('td',{'style':'text-align:center; border-left:none'})
        if(len(td)==1):
            return True
        return False

    def splits_scraper(temp_div):
        tr_list=temp_div.find_all('tr')
        no_of_items=len(tr_list)
        for i in range(1,no_of_items):
            td_list=tr_list[i].find_all('td')
            ca={
                'company_name':td_list[0].getText(),
                'purpose':'SPLITS from Old FV '+td_list[1].getText()+' to New FV '+td_list[2].getText(),
                'anouncment_date':None,
                'record_date':None,
                'ex-date':td_list[3].getText(),
            }
            ca_list.append(ca)

    def dividends_scraper(temp_div):
        tr_list=temp_div.find_all('tr')
        no_of_items=len(tr_list)
        for i in range(1,no_of_items):
            td_list=tr_list[i].find_all('td')
            ca={
                'company_name':td_list[0].getText(),
                'purpose':td_list[1].getText() + ' DIVIDEND of '+td_list[2].getText(),
                'anouncment_date':td_list[3].getText(),
                'record_date':td_list[4].getText(),
                'ex-date':td_list[5].getText(),
            }
            ca_list.append(ca)

    def bonus_scraper(temp_div):
        tr_list=temp_div.find_all('tr')
        no_of_items=len(tr_list)
        for i in range(1,no_of_items):
            td_list=tr_list[i].find_all('td')
            ca={
                'company_name':td_list[0].getText(),
                'purpose':'BONUS RATIO of '+td_list[1].getText(),
                'anouncment_date':td_list[2].getText(),
                'record_date':td_list[3].getText(),
                'ex-date':td_list[4].getText(),
            }
            ca_list.append(ca)

    def rights_scraper(temp_div):
        tr_list=temp_div.find_all('tr')
        no_of_items=len(tr_list)
        for i in range(1,no_of_items):
            td_list=tr_list[i].find_all('td')
            ca={
                'company_name':td_list[0].getText(),
                'purpose':'RIGHTS RATIO of '+td_list[1].getText()+' with PREMIUM of '+td_list[2].getText(),
                'anouncment_date':td_list[3].getText(),
                'record_date':td_list[4].getText(),
                'ex-date':td_list[5].getText(),
            }
            ca_list.append(ca)


    bonus_div_is_empty=check_if_div_empty(bonus_div)
    splits_div_is_empty=check_if_div_empty(splits_div)
    rights_div_is_empty=check_if_div_empty(rights_div)
    dividends_div_is_empty=check_if_div_empty(dividends_div)

    if(not splits_div_is_empty):
        splits_scraper(splits_div)
    if(not dividends_div_is_empty):
        dividends_scraper(dividends_div)
    if(not rights_div_is_empty):
        rights_scraper(rights_div)
    if(not bonus_div_is_empty):
        bonus_scraper(bonus_div)

    return ca_list
