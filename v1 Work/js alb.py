import os
import time
os.environ["PATH"] += os.pathsep + r'D:\PYTHON\projet dl\drivers selenium'

from selenium import webdriver

from bs4 import BeautifulSoup
import urllib.request as urllib2 # import the library used to query a website

url = "http://milesofmusik.com/music_catalog/album-1504826/" #1-Revolution

driver = webdriver.Chrome()
driver.implicitly_wait(30)
driver.get(url)

page = urllib2.urlopen(url)
soup = BeautifulSoup(page, "lxml")

# we first search without having loaded the song
waveform = soup.find('div', {"id": "waveform"})
print(waveform)

# we click on the player
content = driver.find_element_by_class_name("track-play")
content.click()
'''
# we then pause the song
content = driver.find_element_by_class_name("player_play player_pause")
content.click()'''

# second attempt
soup = BeautifulSoup(driver.page_source, "lxml")
print(soup.find('audio'))
waveform = soup.find('div', {"id": "waveform"})
print(waveform)

#driver.close()


