import requests
from bs4 import BeautifulSoup as soup
from selenium import webdriver

from bsedata.bse import BSE
b = BSE()
#b.updateScripCodes()#Updating the skt.json file
print(b.getScripCodes())

