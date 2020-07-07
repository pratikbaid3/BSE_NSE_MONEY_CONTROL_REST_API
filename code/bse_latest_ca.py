import requests
import json
from bs4 import BeautifulSoup as soup
from selenium import webdriver
import sqlite3

def latest_ca():
    conn=sqlite3.connect('corporate_action.db')
    c=conn.cursor()
    c.execute('SELECT * FROM latest_bse_ca')
    ca_array=[]
    for data in c:
        corporate_action={
            'security_code':data[0],
            'security_name':data[1],
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