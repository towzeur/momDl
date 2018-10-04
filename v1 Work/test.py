# import the Beautiful soup functions to parse the data returned from the website
from bs4 import BeautifulSoup
# import the library used to query a website
import urllib.request as urllib2

# 1 Revolution
# Regret & Loss 1
url = "http://milesofmusik.com/music_catalog/album-156591"

# Query the website and return the html to the variable 'page'
page = urllib2.urlopen(url)
# Parse the html in the 'page' variable, and store it in Beautiful Soup format
soup = BeautifulSoup(page, "lxml")

print(soup.prettify())

# tr-156581

# storage/tracks/1RM/015/1RM-015_01 Fading Hopes Full.mp3
# storage/tracks/1RM/015/1RM-015_03 Fading Hopes No Harp.mp3

# storage/tracks/1RM/015/1RM-015_63 Dearly Departed No Str.mp3


# storage/tracks/1M1/014/1M1-014_01 World Stage.mp3

alb = "1M1",
albNum = "014",
trackNum = "01",
trackName = "World Stage"
format0 = "storage/tracks/{alb}/{albNum}/{alb}-{albNum}_{trackNum} {trackName}.mp3".format(alb="1M1",
                                                                                           albNum="014",
                                                                                           trackNum="01",
                                                                                           trackName="World Stage")
print(format0)

# soup.mom-table-header
'''
# soup.find()
content = soup.find(id='content-content')
# print(content)

albumTitle = soup.findAll("div", {"class": "mom-table-header"})[0].string[6:]
# print(albumTitle)

# on s'interesse maintenant au tableau
table = soup.find('table', attrs={'class': 'sticky-enabled'})
# print(table)

tableBody = table.find('tbody')
rows = tableBody.find_all('tr')'''

if __name__ == '__main___':
    pass
    url = "http://milesofmusik.com/music_catalog/album-156591/#tr-156581"
