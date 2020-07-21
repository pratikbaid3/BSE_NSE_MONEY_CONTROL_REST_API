import os
import json
import warnings
import pandas as pd

def process_json_file():
    directory = os.path.dirname(os.path.realpath(__file__))
    json_path = os.path.join(directory, 'jpmorgan_company_list.json')
    if not os.path.exists(json_path):
        warnings.warn("JP Morgan Company List does not exist")
        return []
    with open(json_path) as json_file:
        data = json.load(json_file)
    return data

def process_data():
    df = pd.DataFrame(process_json_file())
    df = df.drop_duplicates(subset=['Symbol'])
    return df.to_dict('records')

def get_company_list():
    return process_data()

