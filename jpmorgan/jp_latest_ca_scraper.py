import requests
import json
import datetime


class JPMorganScraper():

    def __init__(self):
        self.data = []
        self.INITIAL_LINK = "https://api.markitdigital.com/jpmadr-public/v1/corporateActions?limit=1&offset=0"
        self.FINAL_LINK = "https://api.markitdigital.com/jpmadr-public/v1/corporateActions?sortBy=announcementDate&sortOrder=desc&limit={}&offset=0"
        self.LIMIT = None
        self.HEADERS = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        }
        self.company_list = []

    def get_total_limit(self):
        res = requests.get(self.INITIAL_LINK, headers=self.HEADERS)
        data = res.json()
        pagination_details = data['data']['pagination']
        total_items = pagination_details['totalItems']
        self.LIMIT = total_items

    def convert_time(self, time_string):
        dt = datetime.datetime.strptime(time_string, '%Y-%m-%dT%H:%M:%S.000Z')
        return dt.strftime("%Y-%b-%d")

    def scrape_data(self):
        res = requests.get(self.FINAL_LINK.format(
            self.LIMIT), headers=self.HEADERS)
        data = res.json()
        ca_list = data['data']['items']
        for ca in ca_list:
            obj = {}
            obj['Symbol'] = ca.get('ticker', None)
            obj['Company Name'] = ca.get('name', None)
            if not ca.get('action', None):
                continue
            obj['Purpose'] = fr"{ca.get('status', '')} {ca['action']}"
            if not ca.get('announcementDate', None):
                obj['Record Date'] = None
            else:
                obj['Record Date'] = self.convert_time(ca['announcementDate'])
            if not ca.get('eventDate', None):
                continue
            obj['Ex-Date'] = self.convert_time(ca['eventDate'])
            self.data.append(obj)

    def get_latest_ca(self):
        self.get_total_limit()
        self.scrape_data()
        return self.data

    def convert_to_json_file(self, filename="jp.json", encoding="utf-8"):
        with open(filename, "w") as json_file:
            json.dump(self.data, json_file, indent=4, ensure_ascii=False)

	"""
    def convert_to_json_file1(self, filename="jpmorgan_company_list.json", encoding="utf-8"):
        with open(filename, "w") as json_file:
            json.dump(self.company_list, json_file,
                      indent=4, ensure_ascii=False)

    def get_company_list(self):
        for data in self.data:
            obj = {}
            if all([data['Symbol'], data['Company Name']]):
                obj['Symbol'] = data['Symbol']
                obj['Company Name'] = data['Company Name']
                self.company_list.append(obj)
	"""


# j = JPMorganScraper()
# j.get_latest_ca()
