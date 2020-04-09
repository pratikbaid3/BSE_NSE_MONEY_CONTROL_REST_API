import latest_ca_scraper

def main():
    print("----------MENU----------")
    print("1. Latest corporate action")
    choice=int(input("Enter your choice: "))

    if(choice==1):
        print(latest_ca_scraper.latest_ca_scrape())

if __name__ == "__main__":
    main()