import requests
import json
from bs4 import BeautifulSoup as soup

def money_control_ca_scraper():
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
            for td in td_list:
                print(td.getText())
            print()

    def dividends_scraper(temp_div):
        tr_list=temp_div.find_all('tr')
        no_of_items=len(tr_list)
        for i in range(1,no_of_items):
            td_list=tr_list[i].find_all('td')
            for td in td_list:
                print(td.getText())
            print()

    def bonus_scraper(temp_div):
        tr_list=temp_div.find_all('tr')
        no_of_items=len(tr_list)
        for i in range(1,no_of_items):
            td_list=tr_list[i].find_all('td')
            for td in td_list:
                print(td.getText())
            print()

    def rights_scraper(temp_div):
        tr_list=temp_div.find_all('tr')
        no_of_items=len(tr_list)
        for i in range(1,no_of_items):
            td_list=tr_list[i].find_all('td')
            for td in td_list:
                print(td.getText())
            print()


    bonus_div_is_empty=check_if_div_empty(bonus_div)
    splits_div_is_empty=check_if_div_empty(splits_div)
    rights_div_is_empty=check_if_div_empty(rights_div)
    dividends_div_is_empty=check_if_div_empty(dividends_div)

    if(not splits_div_is_empty):
        print("-----SPLIT-----")
        splits_scraper(splits_div)
    if(not dividends_div_is_empty):
        print("-----DIVIDENE-----")
        dividends_scraper(dividends_div)
    if(not rights_div_is_empty):
        print("-----RIGHTS-----")
        rights_scraper(rights_div)
    if(not bonus_div_is_empty):
        print("-----BONUS-----")
        bonus_scraper(bonus_div)



