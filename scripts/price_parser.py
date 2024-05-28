import time
import re

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from auto_chromedriver.driver import Driver

cur_url = ''


def price_parse(art):
    driver = Driver()
    url = 'https://www.ozon.com'
    driver.get(url)

    time.sleep(2)

    element = driver.find_element(By.NAME, "text")

    element.click()

    element.send_keys(art)

    element.send_keys(Keys.ENTER)

    driver.find_element(By.CSS_SELECTOR, "span.tsBody500Medium").click()
    set_cur_url(driver.current_url)

    html_price = driver.find_element(By.CSS_SELECTOR, 'span.l5z.zl5.l9z')

    html_code = html_price.get_attribute('outerHTML')
    soup = BeautifulSoup(html_code, 'html.parser')

    price_string = soup.get_text()

    match = re.findall(r'\d', price_string)
    number_string = ''.join(match)
    price = int(number_string)
    driver.close()
    driver.quit()

    return price


def get_cur_url():
    global cur_url
    return cur_url


def set_cur_url(url):
    global cur_url
    cur_url = url
