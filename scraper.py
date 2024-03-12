from classes.Scraper import Scraper

scraper = Scraper()

try:
    products_csv = scraper.get_input_csv_file()
    urls = scraper.get_url_from_csv_file(products_csv)
    products = scraper.scrape(urls)
    scraper.store_scraped_data_to_file(products)
except Exception as exp:
    print(f"{exp}")