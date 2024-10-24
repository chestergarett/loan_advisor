from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

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
        print('soup',soup)
        # Extracting all items with a specific class
        page_text = soup.get_text()
        data = page_text.strip()
        
        return data

    def scrape_from_file(self, file_path):
        # Read URLs from a text file and scrape each page
        with open(file_path, 'r') as file:
            urls = file.readlines()
        
        for url in urls:
            url = url.strip()
            if url:
                print(f"Scraping: {url}")
                self.navigate_to_page(url)
                data = self.extract_data()
                print(f"Data extracted from {url}: {data}")
            
                self.save_data(url, data)
                
        self.quit()

    def save_data(self, url, data):
        # Save scraped data to a file
        with open(r'data/outputs/scraped_data.txt', 'a') as file:
            file.write(f"Data from {url}:\n")
            for item in data:
                file.write(f"{item}\n")
            file.write("\n")

    def quit(self):
        # Quit the WebDriver
        self.driver.quit()

 # File containing the URLs to scrape
if __name__ == "__main__":
    scraper = WebScraper()
    scraper.scrape_from_file(r'data/inputs/websites_test.txt') 
