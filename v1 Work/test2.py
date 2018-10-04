# import the Beautiful soup functions to parse the data returned from the website
from bs4 import BeautifulSoup
# import the library used to query a website
import urllib.request as urllib2

# 1 Revolution
# Regret & Loss 1
url = 'http://milesofmusik.com/music_catalog/library-155367/'

# Query the website and return the html to the variable 'page'
page = urllib2.urlopen(url)
# Parse the html in the 'page' variable, and store it in Beautiful Soup format
soup = BeautifulSoup(page, "lxml")

#print(soup.prettify())

albumTitle = soup.findAll("span", {"class":"title"})
print(albumTitle)
print(len(albumTitle))

