import time
import re
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from auto_chromedriver.driver import Driver


class OzonParser:
    def __init__(self, art):
        self.art = art
        self.driver = Driver()
        self.url = 'https://www.ozon.com'
        self.driver.get(self.url)
        time.sleep(2)
        self._parse()

    def _parse(self):
        element = self.driver.find_element(By.NAME, "text")
        element.click()
        element.send_keys(self.art)
        element.send_keys(Keys.ENTER)
        time.sleep(2)

        self.driver.find_element(By.CSS_SELECTOR, "span.tsBody500Medium").click()
        time.sleep(2)

        self.current_url = self.driver.current_url

        html_price = self.driver.find_element(By.CSS_SELECTOR, 'span.z7l_27.lz8_27.mm3_27')
        html_code = html_price.get_attribute('outerHTML')
        soup = BeautifulSoup(html_code, 'html.parser')
        price_string = soup.get_text()
        match = re.findall(r'\d', price_string)
        number_string = ''.join(match)
        self.price = int(number_string)

        html_name = self.driver.find_element(By.CSS_SELECTOR, 'h1.mm8_27.tsHeadline550Medium')
        self.product_name = html_name.get_attribute('innerText').strip()

        self.driver.close()
        self.driver.quit()

    def get_price(self):
        return self.price

    def get_product_name(self):
        return self.product_name

    def get_current_url(self):
        return self.current_url


class Product:
    def __init__(self, art):
        self.parser = OzonParser(art)
        self.name = self.parser.get_product_name()
        self.price = self.parser.get_price()
        self.url = self.parser.get_current_url()

    def display_info(self):
        return {
            "name": self.name,
            "price": self.price,
            "url": self.url
        }
