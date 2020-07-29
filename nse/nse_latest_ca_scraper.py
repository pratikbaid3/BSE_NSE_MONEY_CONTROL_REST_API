import os
import requests
from bs4 import BeautifulSoup as bs4
import warnings
import json
import sqlite3
import os
import subprocess
import datetime


class NSEScraper:
    def __init__(self):
        self.data = []
        self.driver = None
        self.soup = None
        self.NSE_URL = (
            "https://www.nseindia.com/api/corporates-corporateActions?index={}"
        )
        self.data_format_from_json = [
            "symbol",
            "comp",
            "series",
            "faceVal",
            "subject",
            "exDate",
            "recDate",
            "bcStartDate",
            "bcEndDate",
        ]
        self.data_format = [
            "Symbol",
            "Company Name",
            "Series",
            "Face Value",
            "Purpose",
            "Ex-Date",
            "Record Date",
            "BC Start-Date",
            "BC End-Date",
        ]

    def __str__(self):
        return "NSE Scraper"

    def __repr__(self):
        return "NSE Scraper()"

    def get_data(self):
        return self.data

    def get_json_data(self):
        json_data = json.dumps(self.get_data())
        return json_data

    def convert_to_json_file(self, filename="nse.json", encoding="utf-8"):
        with open(filename, "w") as json_file:
            json.dump(self.get_data(), json_file, indent=4, ensure_ascii=False)

    def get_data_text(self, text):
        not_present = ["-"]
        if text is None:
            return None
        if text in not_present:
            return None
        return text.strip()

    def scrape_data(self):
        action_type = ["equities", "debt", "mf", "sme"]
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,bn-IN;q=0.8,bn;q=0.7,la;q=0.6",
            "Scheme": "https",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Authority": "www.nseindia.com",
            "Cache-Control": "max-age=0",
        }
        for typ in action_type:
            # res = requests.get(
            #     self.NSE_URL.format(typ), headers=headers,
            # )
            # res.raise_for_status()
            os.popen(f'curl "{self.NSE_URL.format(typ)}" -H "cache-control: max-age=0" -H "dnt: 1" -H "upgrade-insecure-requests: 1" -H "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36" -H "sec-fetch-user: ?1" -H "accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9" -H "sec-fetch-site: none" -H "sec-fetch-mode: navigate" -H "accept-encoding: gzip, deflate, br" -H "accept-language: en-US,en;q=0.9,hi;q=0.8" --compressed  -o api.json').read()
            with open('api.json','r') as api:
                res = json.load(api)
            for data in res:
                temp_data = {}
                for index, data_format_type in enumerate(self.data_format):
                    temp_data[f"{data_format_type}"] = self.get_data_text(
                        data[f"{self.data_format_from_json[index]}"]
                    )
                self.data.append(temp_data)

    def get_corporate_actions(self):
        self.scrape_data()
        return self.data


def mergeData(currData=[]):
    old_data_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "nse_old.json"
    )
    if not os.path.exists(old_data_path):
        warnings.warn("Scraped data for previous NSE Website is not present.")
        return currData

    prevData = []
    with open(old_data_path) as fd:
        prevData = json.load(fd)
    return [*currData, *prevData]


nse = NSEScraper()
currData = nse.get_corporate_actions()
nse_data_list = mergeData(currData)

print(nse_data_list)

# Initializing DB
conn = sqlite3.connect("corporate_action.db")
c = conn.cursor()
c_new = conn.cursor()
create_table = "CREATE TABLE IF NOT EXISTS latest_nse_ca (key text PRIMARY KEY UNIQUE,symbol text, company_name text, series text, face_value text, purpose text,ex_date DATE,record_date text,bc_start_date text,bc_end_date text)"
c.execute(create_table)

# Transfering the data of the latest corporate action to the storage
create_table = "CREATE TABLE IF NOT EXISTS nse_ca (key text PRIMARY KEY UNIQUE,symbol text, company_name text, series text, face_value text, purpose text,ex_date DATE,record_date text,bc_start_date text,bc_end_date text)"
c_new.execute(create_table)
c_new.execute("SELECT * FROM latest_nse_ca")
add_data_to_db = "INSERT INTO nse_ca VALUES (?,?,?,?,?,?,?,?,?,?)"
for data in c_new:
    try:
        c.execute(
            add_data_to_db,
            (
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6],
                data[7],
                data[8],
                data[9],
            ),
        )
    except:
        print("Skipped")

# Deleting the pre-existing data from the database
c.execute("DELETE FROM latest_nse_ca")


# Refreshing the latest ca db
add_data_to_db = "INSERT INTO latest_nse_ca VALUES (?,?,?,?,?,?,?,?,?,?)"

for nse_data in nse_data_list:
    if nse_data["Ex-Date"] != None:
        key = nse_data["Symbol"] + nse_data["Purpose"] + nse_data["Ex-Date"]
        try:
            c.execute(
                add_data_to_db,
                (
                    key,
                    nse_data["Symbol"],
                    nse_data["Company Name"],
                    nse_data["Series"],
                    nse_data["Face Value"],
                    nse_data["Purpose"],
                    # nse_data["Ex-Date"],
                    datetime.datetime.strptime(nse_data["Ex-Date"], "%d-%b-%Y").strftime("%Y-%m-%d"),
                    nse_data["Record Date"],
                    nse_data["BC Start-Date"],
                    nse_data["BC End-Date"],
                ),
            )
        except:
            print(nse_data)
    else:
        pass
conn.commit()
conn.close()

print("Scraped Data Successfully")
