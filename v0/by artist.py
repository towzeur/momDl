from bs4 import BeautifulSoup
import urllib.request as urllib2

from script import main, convertToValidPath

########### CONFIG ############

# to artist
site = 'http://www.milesofmusik.com/music-albums/506457-8'

######### END CONFIG ##########

base = 'http://www.milesofmusik.com'

page = urllib2.urlopen(site)

# Parse the html in the 'page' variable, and store it in Beautiful Soup format
soup = BeautifulSoup(page, "lxml")

nbPage = len(soup.findAll('li', attrs={'class': 'pager-item'}))

#artist
artist = soup.find('div', attrs={'id': 'breadcrumb'}).findAll('a')[1].string
artist = convertToValidPath(artist, prefix='Artist')

try:
    site = site.split('?')[0]
except:
    pass

ALB = []

for i in range(nbPage + 1):

    url = site + '?page=' + str(i)

    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, "lxml")

    catalogItems = soup.find('div', attrs={'class': 'catalog-items'})

    for catalogItem in catalogItems:

        l = catalogItem.find('a')
        try:
            ALB.append(l['href'])
        except:
            pass

ALB = set(ALB)
print(artist, '\n')

for alb in set(ALB):
    url = base + alb
    main(url, p0=artist)
