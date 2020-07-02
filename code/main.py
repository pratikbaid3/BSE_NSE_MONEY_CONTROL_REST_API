import bse_latest_ca_scraper
import bse_particular_company_ca_scraper
import money_control_upcoming_ca_scraper

def main():
    print("----------MENU----------")
    print("1. Latest corporate action")
    print("2. Corporate action of a perticulat company")
    choice=int(input("Enter your choice: "))

    if(choice==1):
        print(bse_latest_ca_scraper.latest_ca_scrape())
    elif(choice==2):
        money_control_upcoming_ca_scraper.money_control_ca_scraper()
if __name__ == "__main__":
    main()

"""Nestle India Ltd.
500790"""