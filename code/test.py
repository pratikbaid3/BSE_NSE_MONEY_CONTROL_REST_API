import requests
import json
from bs4 import BeautifulSoup as soup
from selenium import webdriver
res = requests.get('https://www.bseindia.com/corporates/corporate_act.aspx',headers={'User-Agent':'Mozilla/5.0'})
res.raise_for_status()
page_soup = soup(res.content,features='lxml')