from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json
import os
import re

class WebScraper:
    def __init__(self):
        #  WebDriver Initialization for Selenium.
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    def navigate_to_page(self, url):
        # Specified URL using Selenium.
        self.driver.get(url)
        time.sleep(3)  

    def extract_data(self):
        # Extract data from the loaded webpage using Beautiful Soup.
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        # Extracting all items with a specific class
        page_text = soup.get_text()
        data = f'{page_text.strip()}'
        
        return data

    def clean_text(self, text, keep_chars=[".", ",", " "]):
        pattern = f"[^{''.join(re.escape(char) for char in keep_chars)}a-zA-Z0-9]"
        cleaned_text = re.sub(pattern, "", text)
        cleaned_text = re.sub(r"\s+", " ", cleaned_text)
        cleaned_text = cleaned_text.strip()
        
        return cleaned_text

    def scrape_from_file(self, input_path,output_path):
        # Read URLs from a text file and scrape each page
        with open(input_path, 'r') as file:
            urls = file.readlines()
        
        for url in urls:
            url = url.strip()
            if url:
                print(f"Scraping: {url}")
                self.navigate_to_page(url)
                data = self.extract_data()
                cleaned_data = self.clean_text(data)
                self.save_data(url, cleaned_data,output_path)
                print(f'Scraping: File saved to JSON')
        self.quit()

    def save_data(self, url, data,output_path):
        # Save scraped data to a file
        if os.path.exists(output_path):
            with open(output_path, 'r') as json_file:
                existing_data = json.load(json_file)
        else:
            existing_data = {}

        existing_data[url] = {'content': data}

        with open(output_path, 'w') as json_file:
            json.dump(existing_data, json_file)

    def quit(self):
        # Quit the WebDriver
        self.driver.quit()

 # File containing the URLs to scrape
if __name__ == "__main__":
    INPUT_PATH = r'data/inputs/websites/websites_test.txt'
    OUTPUT_PATH = r'data/outputs/scraped_data.json'
    scraper = WebScraper()
    scraper.scrape_from_file(INPUT_PATH,OUTPUT_PATH) 
