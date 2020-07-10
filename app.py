from flask import Flask,request
from flask_restful import Api, Resource, reqparse
from flask_jwt import JWT
import requests
import json
from bs4 import BeautifulSoup as soup
from selenium import webdriver
import os
from bse import bse_latest_ca_scraper
from bse import bse_company_ca_scraper
from bse import bse_latest_ca
from bse import bse_company_ca

app=Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS']=True
app.secret_key='Pratik'
api=Api(app)

#Latest corporate action from the database(Server)
class LatestCA(Resource):
    def get(self):
        return{'latest_ca':bse_latest_ca.latest_ca()}

#Particular company corporate action from historical data
class CompanyCA(Resource):
    def get(self,code):
        return{'ca':bse_company_ca.company_ca(code)}


#Particular company corporate action (Scraper & Server)
class CompanyCAScraper(Resource):
    def get(self,name,code):
        return {'company_ca':bse_company_ca_scraper.company_ca_scraper(name,code)}

#Scraper for latest croporate action(Scraper)
class LatestCAScraper(Resource):
    def get(self):
        return {'message':bse_latest_ca_scraper.latest_ca_scrape()}
        

api.add_resource(LatestCA,'/api/latestca')
api.add_resource(CompanyCA,'/api/companyca/<string:code>')
api.add_resource(CompanyCAScraper,'/api/companycascraper/<string:name>/<string:code>')
api.add_resource(LatestCAScraper,'/api/latestcascraper')

if __name__=='__main__':
    app.run(port=5000,debug=True)