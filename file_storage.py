import pandas as pd
import base64
import os
import pdfkit

from nse import nse_latest_ca
from bse import bse_latest_ca
from money_control import money_control_upcoming_ca

def store_file_as_csv_pdf():
    filename = "Latest Corporate Actions"

    store_file(f"{filename} BSE.csv", bse_latest_ca.latest_ca())
    store_file(f"{filename} BSE.pdf", bse_latest_ca.latest_ca(), 'pdf')

    store_file(f"{filename} NSE.csv", nse_latest_ca.latest_ca())
    store_file(f"{filename} NSE.pdf", nse_latest_ca.latest_ca(), 'pdf')

    store_file(f"{filename} MC.csv", money_control_upcoming_ca.latest_ca())
    store_file(f"{filename} MC.pdf", money_control_upcoming_ca.latest_ca(), 'pdf')


def store_file(filename, data, typ="csv"):
    if typ == 'csv':
        df=pd.DataFrame(data=data)
        df.index+=1
        if not os.path.exists(os.path.join('public')):
            os.makedirs(os.path.join('public'))
        file_path = os.path.join('public/', filename)
        df.to_csv(file_path)
        return True
    elif typ == 'pdf':
        df=pd.DataFrame(data=data)
        directory = os.path.dirname(os.path.realpath(__file__))
        if not os.path.exists(os.path.join('public')):
            os.makedirs(os.path.join('public'))
        html_file_path = os.path.join('public', "LatestCorporateActions.html")
        pdf_file_path = os.path.join('public', filename)
        fd = open(html_file_path,'w')
        intermediate = df.to_html()
        fd.write(intermediate)
        fd.close()
        pdfkit.from_file(html_file_path, pdf_file_path)

store_file_as_csv_pdf()