import requests
from bs4 import BeautifulSoup as soup
res = requests.get('https://www.bseindia.com/corporates/corporate_act.aspx')
res.raise_for_status()
page_soup = soup(res.content,features='lxml')
allLinks=page_soup.find_all('td',{"class":"TTRow_left"})
noOfLinks=len(allLinks)

corporate_act={}

i=0
while(i<noOfLinks):
    corporate_act[allLinks[i].text]=allLinks[i+1].text
    print(allLinks[i].text)
    i=i+2

print(corporate_act)