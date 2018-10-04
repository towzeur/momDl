from bs4 import BeautifulSoup
import urllib.request as urllib2

from cnst import *


def scrapAlbum(url):
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, "lxml")

    '''getting all the trackname(sorted)'''
    tracks = soup.find('div', {"class": "table tracklisttable"}).findAll('div', {"class": 'tr'})
    tracklist = []
    for track in tracks:
        tracklist.append(track.find('a', {"class": "nameTrackList"}).text)  # trackName
        # track.find('div', {"class": "td no-mb"}).text    # trackNum

    ''' Album info : artist and alb name '''
    tmpAlb = soup.find("div", {'class': "breadcrumbs container"})
    albTitle = tmpAlb.span.text
    albArtist = tmpAlb.findAll('a')[2].text

    ''' We get the cover path '''
    coverPath = soup.find('img', {"title": albTitle})["src"]

    return {'title': tmpAlb.span.text,
            'artist': albArtist,
            'cover': coverPath,
            'tracklist': tracklist}


if __name__ == "__main__":


    url = "http://milesofmusik.com/music_catalog/album-791685/"

    ALB = scrapAlbum(url)

    import pprint
    pprint.pprint(ALB)

    '''
    {'artist': 'Ninja Tracks',
     'cover': 'storage/albums/07/28/02/20/210_210_5af1a25d820be.jpg',
     'title': 'Revolution Tools',
     'tracklist': ['Aeron Rise',
                   'Cleave Rise',
                   'Cut Rise',
                   'Icy Rise',
     ...
    
    '''
