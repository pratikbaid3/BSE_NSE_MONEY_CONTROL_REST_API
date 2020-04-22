import requests
import json
from bs4 import BeautifulSoup as soup

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


bonus_div_is_empty=check_if_div_empty(bonus_div)
splits_div_is_empty=check_if_div_empty(splits_div)
rights_div_is_empty=check_if_div_empty(rights_div)
dividends_div_is_empty=check_if_div_empty(dividends_div)


print(bonus_div_is_empty)
print(splits_div_is_empty)
print(rights_div_is_empty)
print(dividends_div_is_empty)
