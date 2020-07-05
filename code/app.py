from flask import Flask,request
from flask_restful import Api, Resource, reqparse
from flask_jwt import JWT
import requests
import json
from bs4 import BeautifulSoup as soup
from selenium import webdriver
import bse_latest_ca_scraper
import bse_company_ca_scraper

app=Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS']=True
app.secret_key='Pratik'
api=Api(app)

class LatestCA(Resource):
    def get(self):
        return {'latest_ca': bse_latest_ca_scraper.latest_ca_scrape()}

class CompanyCA(Resource):
    def get(self,name,code):
        return {'latest_ca':bse_company_ca_scraper.company_ca_scraper(name,code)}

api.add_resource(LatestCA,'/latestca')
api.add_resource(CompanyCA,'/companyca/<string:name>/<string:code>')

if __name__=='__main__':
    app.run(port=5000,debug=True)