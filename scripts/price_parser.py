import asyncio
import time
import re
from bs4 import BeautifulSoup
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from auto_chromedriver.driver import Driver
from undetected_chromedriver.options import ChromeOptions


def find_element_safe(driver, by, value):
    try:
        return driver.find_element(by, value)
    except NoSuchElementException:
        raise NoSuchElementException(f"Element with {by}='{value}' not found")


def find_elements_safe(driver, by, value):
    try:
        elements = driver.find_elements(by, value)
        if not elements:
            raise NoSuchElementException(f"Elements with {by}='{value}' not found")
        return elements
    except NoSuchElementException:
        raise NoSuchElementException(f"Elements with {by}='{value}' not found")


class OzonParser:
    def __init__(self, art, is_for_art, url):
        self.is_for_art = is_for_art
        self.art = art
        options = ChromeOptions()
        options.add_argument(f"--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
                             f"like Gecko) Chrome/126.0.0.0 Safari/537.36")
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        self.driver = Driver(options=options)
        self.url = url
        if is_for_art:
            self.driver.get('https://ozon.com')
        else:
            self.driver.get(self.url)
        time.sleep(2)
        self._parse()

    def _parse(self):
        try:
            if self.is_for_art:
                element = self.driver.find_element(By.NAME, "text")
                element.click()
                element.send_keys(self.art)
                element.send_keys(Keys.ENTER)
                time.sleep(2)

                product_divs = find_elements_safe(self.driver, By.CSS_SELECTOR, "div.a8b.ba9.ac.i0x_23")
                if product_divs:
                    first_product_div = product_divs[0]
                    first_span = find_element_safe(first_product_div, By.CSS_SELECTOR, "span.tsBody500Medium")
                    first_span.click()
                    time.sleep(2)

                self.current_url = self.driver.current_url
                self._parse_product_card()
            else:
                self.current_url = self.url
                self._parse_product_card()
        except NoSuchElementException as e:
            print(f"Error: {e}")
            self.driver.close()
            self.driver.quit()

    def _parse_product_card(self):
        html_price = find_element_safe(self.driver, By.CSS_SELECTOR, 'span.m5m_27.mm6_27.m1n_27')
        html_code = html_price.get_attribute('outerHTML')
        soup = BeautifulSoup(html_code, 'html.parser')
        price_string = soup.get_text()
        match = re.findall(r'\d', price_string)
        number_string = ''.join(match)
        self.price = int(number_string)

        html_name = find_element_safe(self.driver, By.CSS_SELECTOR, 'h1.n3m_27.tsHeadline550Medium')
        self.product_name = html_name.get_attribute('innerText').strip()

        article_element = find_element_safe(self.driver, By.CSS_SELECTOR, 'button[data-widget="webDetailSKU"] '
                                                                          '.ga14-a2.tsBodyControl400Small')

        article_text = article_element.text
        article_number = article_text.split(": ")[1]

        if not self.is_for_art:
            self.art = article_number

        self.driver.close()
        self.driver.quit()

    def get_price(self):
        return self.price

    def get_product_name(self):
        return self.product_name

    def get_current_url(self):
        return self.current_url


class Product:
    def __init__(self, art, is_for_art, url):
        self.parser = OzonParser(art, is_for_art, url)
        self.name = self.parser.get_product_name()
        self.price = self.parser.get_price()
        self.url = self.parser.get_current_url()

    def display_info(self):
        return {
            "name": self.name,
            "price": self.price,
            "url": self.url,
            "art": self.parser.art
        }

    @classmethod
    async def fetch_product_details(cls, art, is_for_art, url):
        return await asyncio.to_thread(Product, art, is_for_art, url)
