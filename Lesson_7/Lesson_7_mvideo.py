from selenium import webdriver
from pymongo import MongoClient
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import exceptions


client = MongoClient('localhost', 27017)
mongo_base = client['mvideo_db']
collection = mongo_base['hits']

firefox_options = Options()
firefox_options.add_argument("--headless")

driver = webdriver.Firefox(options=firefox_options)

url = 'https://www.mvideo.ru'
title_site = 'М.Видео'

driver.get(url)

assert title_site in driver.title

try:
    hits = driver.find_element_by_xpath(
        '//div[contains(text(),"Хиты продаж")]/ancestor::div[@data-init="gtm-push-products"]'
    )
except exceptions.NoSuchElementException:
    print('There are no sales hits')

while True:
    try:
        next_button = WebDriverWait(hits, 5).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'a[class="next-btn sel-hits-button-next"]')
            )
        )

        driver.execute_script("$(arguments[0]).click();", next_button)
    except exceptions.TimeoutException:
        print('Data collection is finished')
        break

goods = hits.find_elements_by_css_selector('li.gallery-list-item')

attributes = {}
for good in goods:
    attributes['title'] = good.find_element_by_css_selector(
        'a.sel-product-tile-title') \
        .get_attribute('innerHTML')

    attributes['good_link'] = good.find_element_by_css_selector(
        'a.sel-product-tile-title') \
        .get_attribute('href')

    attributes['price'] = float(
        good.find_element_by_css_selector(
            'div.c-pdp-price__current').get_attribute('innerHTML').replace(
                '&nbsp;', '').replace('¤', ''))

    attributes['image_link'] = good.find_element_by_css_selector(
        'img[class="lazy product-tile-picture__image"]') \
        .get_attribute('src')

    collection.update_one({'good_link': attributes['good_link']}, {'$set': attributes},
                          upsert=True)
driver.quit()
