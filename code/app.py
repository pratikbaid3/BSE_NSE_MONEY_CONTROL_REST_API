from flask import Flask,request
from flask_restful import Api, Resource, reqparse
from flask_jwt import JWT
import requests
import json
from bs4 import BeautifulSoup as soup
from selenium import webdriver
import bse_latest_ca_scraper
import bse_particular_company_ca_scraper

app=Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS']=True
app.secret_key='Pratik'
api=Api(app)

class LatestCA(Resource):
    def get(self):
        return {'latest ca': bse_latest_ca_scraper.latest_ca_scrape()}

class ParticularCompanyCA(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument(
        'secuarity_name',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument(
        'secuarity_code',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    def get(self,name):
        data=ParticularCompanyCA.parser.parse_args()
        securaity_name=data['secuarity_name']
        secuarity_code=data['secuarity_code']
        return({f'Ca of {name}':bse_particular_company_ca_scraper.companyDataScraper(secuarity_code,securaity_name,'01/01/2015')})

api.add_resource(LatestCA,'/latestca')
api.add_resource(ParticularCompanyCA,'/companyca/<string:name>')

if __name__=='__main__':
    app.run(port=5000,debug=True)