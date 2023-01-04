#https://stackoverflow.com/questions/72062123/beautifulsoup-find-all-function-returns-eempty-list
#https://github.com/CyberPunkMetalHead/binance-trading-bot-new-coins

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from chromedriver_py import binary_path
import os.path, json

from store_order import *
from load_config import *
#from send_notification import *

from datetime import datetime, time
import time
from bs4 import BeautifulSoup as bs

def get_all_announce():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service_object = Service(binary_path)
    driver = webdriver.Chrome(service=service_object)
    #driver = webdriver.Chrome(executable_path=binary_path, options=chrome_options)
    driver.get("https://www.binance.com/en/support/announcement/c-48?navId=48")
    driver.implicitly_wait(10)

    """
    html = driver.page_source
    soup = bs(html)
    for tag in soup.find_all("div", class_="css-1q4wrpt"):
        print(tag.text)
        print('aaa')
    driver.close()
    """
    #latest_announcement = driver.find_element(By.ID, 'link-0-0-p1')
    announce_list = []
    search = driver.find_elements(By.XPATH, '//div[@class="css-1q4wrpt"]')
    for parents in search:
        spans = parents.find_elements(By.XPATH, './/div[@class="css-f94ykk"]')
        for span in spans:
            if span.text != '':
                print(span.text)
                announce_list.append(span.text)
    driver.close()
    return announce_list
    
def get_last_coin():
    announce_list = get_all_announce()
    
    print(len(announce_list))
    if len(announce_list) <= 0:
        return
    
    latest_announcement = announce_list[0]
    print(latest_announcement)

    # Binance makes several annoucements, irrevelant ones will be ignored
    exclusions = ['Futures', 'Margin', 'adds']
    for item in exclusions:
        if item in latest_announcement:
            return None
    enum = [item for item in enumerate(latest_announcement)]
    #Identify symbols in a string by using this janky, yet functional line
    uppers = ''.join(item[1] for item in enum if item[1].isupper() and (enum[enum.index(item)+1][1].isupper() or enum[enum.index(item)+1][1]==' ' or enum[enum.index(item)+1][1]==')') )
    print(uppers)
    return uppers


def store_new_listing(listing):
    """
    Only store a new listing if different from existing value
    """

    if os.path.isfile('new_listing.json'):
        file = load_order('new_listing.json')
        if listing in file:
            print("No new listings detected...")

            return file
        else:
            file = listing
            store_order('new_listing.json', file)
            #print("New listing detected, updating file")
            #send_notification(listing)
            return file

    else:
        new_listing = store_order('new_listing.json', listing)
        #send_notification(listing)
        #print("File does not exist, creating file")

        return new_listing


def search_and_update():
    """
    Pretty much our main func
    """
    while True:
        latest_coin = get_last_coin()
        if latest_coin:
            store_new_listing(latest_coin)
        else:
            pass
        print("Checking for coin announcements every 2 hours (in a separate thread)")
        return latest_coin
        time.sleep(60*180)


if __name__ == '__main__':
    print('working...')
    search_and_update()
    #get_all_announce()