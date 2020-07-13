from flask import Flask,request
from flask_restful import Api, Resource, reqparse
from flask_jwt import JWT
import requests
import json
from bs4 import BeautifulSoup as soup
from selenium import webdriver
import os

#BSE Imports
from bse import bse_latest_ca
from bse import bse_company_ca

#NSE Imports
from nse import nse_latest_ca
from nse import nse_company_ca

#MoneyControl Imports
from money_control import money_control_upcoming_ca
from money_control import money_control_company_ca

app=Flask(__name__, static_url_path='/public', static_folder='public/')
app.config['PROPAGATE_EXCEPTIONS']=True
app.secret_key='Pratik'
api=Api(app)

#BSE Latest corporate action from the database(Server)
class LatestCA_BSE(Resource):
    def get(self):
        return{'latest_ca':bse_latest_ca.latest_ca()}

#BSE Particular company corporate action from historical data
class CompanyCA_BSE(Resource):
    def get(self,code):
        return{'ca':bse_company_ca.company_ca(code)}

#NSE Latest corporate action from the database
class LatestCA_NSE(Resource):
    def get(self):
        return{'latest_ca':nse_latest_ca.latest_ca()}

#NSE Particular company corporate action from historical data
class CompanyCA_NSE(Resource):
    def get(self,code):
        return{'ca':nse_company_ca.company_ca(code)}

#Money Control Latest corporate action from the database
class LatestCA_MC(Resource):
    def get(self):
        return{'latest_ca':money_control_upcoming_ca.latest_ca()}

#Money Control Particular company corporate action from historical data
class CompanyCA_MC(Resource):
    def get(self,code):
        return{'ca':money_control_company_ca.company_ca(code)}
        

api.add_resource(LatestCA_BSE,'/api/bse_latestca')
api.add_resource(CompanyCA_BSE,'/api/bse_companyca/<string:code>')
api.add_resource(LatestCA_NSE,'/api/nse_latestca')
api.add_resource(CompanyCA_NSE,'/api/nse_companyca/<string:code>')
api.add_resource(LatestCA_MC,'/api/mc_latestca')
api.add_resource(CompanyCA_MC,'/api/mc_companyca/<string:code>')

if __name__=='__main__':
    app.run(port=5000,debug=True)