import datetime
import time

import requests
import selenium.webdriver
from selenium.webdriver.chrome.options import Options
import json

headers = headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

global cookiesc
cookiesc = {}


def updateCookies():
    driver = selenium.webdriver.Chrome()
    driver.get("https://www.vinted.fr/")
    cookies = driver.get_cookies()
    for a in cookies:
        if a['name'] == '_vinted_fr_session': vinted_session = a['value']
        if a['name'] == 'anon_id': anon_id = a['value']
    driver.close()

    token = 'anon_id=' + anon_id + ';' + '_vinted_fr_session=' + vinted_session + ';'

    global cookiesc
    cookiesc = dict(Cookie=token)


def updateData():
    items = {}
    data_tshirts = requests.get(
        "https://www.vinted.fr/api/v2/catalog/items?catalog_ids=76&color_ids=&brand_ids=94,304&size_ids=&material_ids=&status_ids=&is_for_swap=0&order=newest_first&price_to=15",
        headers=headers, cookies=cookiesc)
    data_sneakers = requests.get(
        "http://www.vinted.fr/api/v2/catalog/items?catalog_ids=1242&color_ids=&brand_ids=53,14,304,1775&size_ids=&material_ids=&status_ids=&is_for_swap=0&price_to=&size_ids=790&order=newest_first",
        headers=headers, cookies=cookiesc)
    data_pants = requests.get(
        "https://www.vinted.fr/api/v2/catalog/items?catalog_ids=34&color_ids=&brand_ids=&size_ids=&material_ids=&status_ids=6,1,2&is_for_swap=0&order=newest_first",
        headers=headers, cookies=cookiesc)
    data_accessories = requests.get(
        "https://www.vinted.fr/api/v2/catalog/items?catalog_ids=34,82&color_ids=&brand_ids=&size_ids=&material_ids=&status_ids=6,1,2&is_for_swap=0&order=newest_first",
        headers=headers, cookies=cookiesc)
    data_3d_swhoosh = requests.get(
        "https://www.vinted.fr/api/v2/catalog/items?catalog_ids=1231&search_text=dunk+low&catalog_ids=&currency=EUR&color_ids=&brand_ids=&size_ids=&material_ids=&status_ids=&is_for_swap=0&order=newest_first&price_to=100",
        headers=headers, cookies=cookiesc)
    data_af1 = requests.get(
        "https://www.vinted.fr/api/v2/catalog/items?catalog_ids=1242&search_text=air+force+one+blanche&catalog_ids=&currency=EUR&color_ids=&brand_ids=&size_ids=776,778,1191,789,780,782,784,785,786,787,788,790,791,792,794,1190&material_ids=&status_ids=&is_for_swap=0&order=newest_first&price_to=20",
        headers=headers, cookies=cookiesc)
    try :
        tshirts = data_tshirts.json()
        sneakers = data_sneakers.json()
        pants = data_pants.json()
        accessories = data_accessories.json()
        items['tshirts'] = tshirts['items']
        items['sneakers'] = sneakers['items']
        items['pants'] = pants['items']
        items['accessories'] = accessories['items']
        items['3d_swhoosh'] = data_3d_swhoosh.json()['items']
        items['af1'] = data_af1.json()['items']

    except (Exception):
        print("Error: " + str(Exception))

    with open('data.json', 'w') as outfile:
        json.dump(items, outfile, indent=1)


if __name__ == '__main__':
    while True:
        if datetime.datetime.now().minute ==42:
            updateCookies()

        if len(cookiesc) > 0:
            updateData()

        time.sleep(30)

        
