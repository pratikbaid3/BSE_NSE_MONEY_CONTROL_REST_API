import requests
import json

from selenium import webdriver
from bs4 import BeautifulSoup as bs4

class ScrapeError(Exception):

    def __init__(self, org):
        self.org = org
        self.message = f"Cannot Scrape {org}"
    
    def __str__(self):
        return f"Some error occured while scraping {self.org}"

"""
    Scrapes the NSE Website to get the corporate actions of the companies
"""
class NSEScraper():
    """
        @class variables

        1. NSE_CORPORATE_ACTION_HOMEPAGE_URL
        2. soup
        3. data
        4. data_format
        5. page

        ----------------------

        @USAGE

        # Create an instance of the NSEScraper class
        nse = NSEScraper()

        # Scrape data from NSE website
        nse.get_all_corporate_actions()

        # Get the scraped data
        nse.get_data()

        # Get json data
        nse.get_json_data()

        # Convert into a json file
        nse.convert_to_json_file('filename.json')
    """

    def __init__(self):
        self.NSE_CORPORATE_ACTION_HOMEPAGE_URL = "https://www1.nseindia.com/sme/marketinfo/corporates/actions/latestCorpActions.jsp?currentPage={}"
        self.soup = None
        self.data = []
        self.data_format = [
            'Symbol',
            'Company Name',
            'Series',
            'Face Value',
            'Purpose',
            'Ex-Date',
            'Record Date',
            'BC Start-Date',
            'BC End-Date'
        ]
        self.page = 1

    def __str__(self):
        return "NSE Scraper"

    def __repr__(self):
        return "NSE Scraper()"
    
    def get_data(self):
        return self.data

    def add_soup(self):
        res = requests.get(self.NSE_CORPORATE_ACTION_HOMEPAGE_URL.format(self.page), headers={
                           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'})
        status = res.status_code
        if status == 200:
            self.soup = bs4(res.content, features='lxml')
        else:
            raise ScrapeError("NSE")

    def print_soup(self):
        if __name__ == "__main__":
            print(self.get_soup())

    def setup(self):
        self.add_soup()

    def get_data_text(self, element):
        not_present = ['-']
        if element is None:
            return None
        text = element.getText()
        if text in not_present:
            return None
        return text.strip()

    """
        Scrape data for a particular page
        Returns True if data exists in the page and False if data does not exist
    """
    def scrape_data(self):
        self.setup()
        table = self.soup.find_all('table')[1]
        scraped_corporate_datas = table.find_all('tr')
        if len(scraped_corporate_datas) <= 1:
            return False
        for corporate_data in scraped_corporate_datas:
            scraped_data = corporate_data.find_all('td')
            if len(scraped_data) <= 0:
                continue
            temp_data = {}
            for index, data in enumerate(scraped_data):
                # Two extra columns are present, ND Start Date and ND End Date which is null
                if index < len(self.data_format):
                    textual_data = self.get_data_text(data)
                    temp_data[self.data_format[index]] = textual_data
            self.data.append(temp_data)
        return True
    
    def get_all_corporate_actions(self):
        status = self.scrape_data()
        if status:
            self.page += 1
            self.get_all_corporate_actions()


    def display_data(self):
        if __name__ == "__main__":
            print(self.get_data())

    def get_json_data(self):
        json_data = json.dumps(self.get_data())
        return json_data

    def convert_to_json_file(self, filename="nse.json", encoding='utf-8'):
        with open(filename, 'w') as json_file:
            json.dump(self.get_data(), json_file, indent=4, ensure_ascii=False)

nse = NSEScraper()
nse.get_all_corporate_actions()
nse.convert_to_json_file('nse_old.json')
