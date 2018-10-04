import os
import time

# add the selenium driver
os.environ["PATH"] += os.pathsep + r'..\Web Drivers'

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup

from cnst import *


def scrapArtistLibrary(url):

    ''' # https://intoli.com/blog/running-selenium-with-headless-chrome/'''
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)

    driver.implicitly_wait(30)
    driver.get(url)

    '''we change the view from 18 (default) to 54 (max)'''
    #scroll = driver.find_elements_by_class_name("selectric-input")[1]
    #print(scroll)
    #scroll.send_keys('2')


    while True:  # while we can expand

        python_button = driver.find_element_by_id("showMoreCatalog")

        try:
            python_button.click()
            time.sleep(0.5)
        except:  # if the button isn't visible
            break

    # finaly, the whole artist catalog is printed
    soup = BeautifulSoup(driver.page_source, "lxml")

    # We loop into each alb to scrap alb data
    DATA = []
    for box in soup.findAll('a', {'class': 'box'}):
        d = {"albLink": box['href'],  # /music_catalog/album-155366/
             "coverLink": box.img['src'],  # storage/albums/22/03/22/02/210_210_5af18c796de2a.jpg
             "albName": box.find('span', {'class': 'title'}).find('br').nextSibling,  # Light Tension & Anticipation 1
             "artistCode": box.find('span', {'class': 'title'}).find('br').previous.split('-')[0],  # 1RM
             "albCode": box.find('span', {'class': 'title'}).find('br').previous.split('-')[1]  # 001
             }

        DATA.append(d)

    driver.close()

    return DATA


if __name__ == "__main__":
    import pprint

    # url = "http://milesofmusik.com/music_catalog/library-155367/"  # 1-Revolution
    url = "http://milesofmusik.com/music_catalog/library-791431/"  # ninja

    DATA = scrapArtistLibrary(url)
    yépprint.pprint(DATA)

    '''
    
    [{'albCode': '001',
      'albLink': '/music_catalog/album-791430/',
      'albName': 'Revolution Zero',
      'artistCode': 'NINJAR',
      'coverLink': 'storage/albums/02/08/26/04/210_210_5af1a25d532a9.jpg'},
    ...
    ]
    
    '''
