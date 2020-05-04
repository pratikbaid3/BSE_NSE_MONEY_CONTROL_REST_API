import latest_ca_scraper
import perticular_company_ca_scraper

def main():
    print("----------MENU----------")
    print("1. Latest corporate action")
    print("2. Corporate action of a perticulat company")
    choice=int(input("Enter your choice: "))

    if(choice==1):
        print(latest_ca_scraper.latest_ca_scrape())
    elif(choice==2):
        secuarity_code=input("Enter the secuarity code")
        secuarity_name=input("Enter the secuarity name")
        start_date=input("Enter the start date")
        print(perticular_company_ca_scraper.companyDataScraper(secuarity_code,secuarity_name,start_date))
if __name__ == "__main__":
    main()

"""Nestle India Ltd.
500790"""