from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from pymongo import MongoClient
from selenium.webdriver.firefox.options import Options


def parse_field(element, css_selector):
    result = WebDriverWait(element, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))).text
    return result


def parse_email(field):
    fields = {}

    fields['from_name'] = parse_field(
        field, 'span[class~="ns-view-message-head-sender-name"]')
    fields['from_email'] = parse_field(
        field, 'span[class~="mail-Message-Sender-Email"]')
    fields['date'] = parse_field(field,
                                  'div[class~="ns-view-message-head-date"]')
    fields['subject'] = parse_field(
        field, 'div[class~="mail-Message-Toolbar-Subject"]')
    fields['text_messege'] = parse_field(
        field, 'div.mail-Message-Body-Content')

    return fields


client = MongoClient('localhost', 27017)
mongo_db = client['email_db']
collection = mongo_db['emails']

firefox_options = Options()
firefox_options.add_argument("--headless")

driver = webdriver.Firefox()

url = 'https://yandex.ru/'
title_site = 'Яндекс'

driver.get(url)

assert title_site in driver.title

try:
    mail_button = driver.find_element_by_css_selector(
        'a[class="button desk-notif-card__login-enter-expanded button_theme_gray i-bem"]'
    )
except exceptions.NoSuchElementException:
    print('Mail login not found')

mail_button.click()

driver.title

if 'Авторизация' in driver.title:
    login_form = driver.find_element_by_css_selector('div[class="passp-auth"]')

    login_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'passp-field-login')))
    login_field.send_keys('tibo78')
    login_field.send_keys(Keys.ENTER)
    pwd_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'passp-field-passwd')))
    pwd_field.send_keys('yj7kba')
    pwd_field.send_keys(Keys.ENTER)

first_email = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.CLASS_NAME, 'ns-view-messages-item-wrap')
    )
)
first_email.click()

while True:
    try:
        collection.insert_one(parse_email(driver))

        next_button = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'след.')))
        next_button.click()
    except exceptions.TimeoutException:
        print('No more emails')
        break

driver.quit()
