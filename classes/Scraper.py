from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import sys

class Scraper:
    def get_input_csv_file(self):
        if len(sys.argv) <= 1:
            raise Exception('Error: CSV file was not provided!')
        
        return sys.argv[1]
    

    def get_url_from_csv_file(self, csv_file):
        urls = []

        if os.path.isfile(csv_file) == False:
            raise Exception(f'Error: {csv_file} is not a valid csv file!')
        
        with open(csv_file, newline='') as fh:
            reader = csv.reader(fh)
            for row in reader:
                urls.append(row[0])

        return urls


    def scrape(self, urls):
        products = []

        if len(urls) <= 0:
            raise Exception(f'Error: URLs list is empty!')

        for url in  urls:
            response = requests.get(url)
            html = response.text

            soap = BeautifulSoup(html, 'html.parser')

            title = soap.find('h1', {'class' : 'ty-product-block-title'}).text

            price = soap.find('span', {'class' : 'price_inner--amount'}).span.text

            description = soap.find('div', {'class' : 'ty-product_details-description'}).text
            description = description if len(description) > 1 else "N/D"
            
            image = soap.find('div', {'class' : 'ty-product-img'}).figure
            if image is not None:
                image_url = image.findChild("span")['href']

            products.append([title, description, price, image_url])

            print('Working...')
        
        return products
    

    def generate_filename_from_title(self, title):
        title_wschars = re.sub('[^A-Za-z0-9\ ]+', '', title)
        return re.sub('\ ', '-', title_wschars)
    

    def store_scraped_data_to_file(self, products):
        if len(products) == 0:
            raise Exception('Error: Product list is empty!')
        
        for product in products:
            filename = f'products/{self.generate_filename_from_title(product[0])}.html'
            file_content = f'<h1>{product[0]}</h1> <p>{product[1]}<p> <p>{product[2]} EUR</p> <img src="{product[3]}" width="300" />'
            with open(filename, 'w') as fh:
                fh.write(file_content)
                fh.close()
            print('Saving product data to file...')
        
        print('Done!')
