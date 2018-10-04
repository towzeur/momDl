# mp3 treatment
from mutagen.easyid3 import EasyID3
import mutagen

# import the Beautiful soup functions to parse the data returned from the website
from bs4 import BeautifulSoup
# import the library used to query a website
import urllib.request as urllib2
import requests

import os, errno
import pprint

# multitasking
import concurrent.futures

########### CONFIG ############

# to album
siteALB = 'http://www.milesofmusik.com/music-tracks/852113-13/852576-2'


######### END CONFIG ##########

def getAlbum(site):
    # Query the website and return the html to the variable 'page'
    page = urllib2.urlopen(site)

    # Parse the html in the 'page' variable, and store it in Beautiful Soup format
    soup = BeautifulSoup(page, "lxml")

    # print(soup.prettify())

    # soup.mom-table-header

    # soup.find()
    content = soup.find(id='content-content')
    # print(content)

    albumTitle = soup.findAll("div", {"class": "mom-table-header"})[0].string[6:]
    # print(albumTitle)

    # on s'interesse maintenant au tableau
    table = soup.find('table', attrs={'class': 'sticky-enabled'})
    # print(table)

    tableBody = table.find('tbody')
    rows = tableBody.find_all('tr')

    album = {}

    for row in rows:
        track_path = row.find('input', attrs={'name': "track_path"})['value']

        track_title = row.find('input', attrs={'name': "track_title"})['value']

        td = row.find_all('td')

        title = td[1].string
        duration = td[2].string
        track = int(td[3].string)

        # print(title, duration, track)

        album[track] = {'track_path': track_path,
                        'track_title': track_title,
                        'title': title,
                        'length': duration}

    return album, albumTitle


def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e:  # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occurred


def downloadFile(url, file_name):
    r = requests.get(url, stream=True)
    with open(file_name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


def makePath(liste):
    output = ''
    for p in liste:
        if p:
            if (p[-1] in '\/'):
                output += p
            else:
                output += p + '/'
    return output


def findPathName(path='', prefix='Album'):
    i = 0
    base = 'Invalid ' + prefix + ' {}'

    newPath = makePath((path, base.format(i)))

    while os.path.exists(newPath):
        i += 1
        newPath = makePath((path, base.format(i)))

    return newPath


def convertToValidPath(badString, path='', prefix='Album'):
    '''Convert badString to a valid Windows Path'''

    reservedCharacters = '<>:"/\|?*'
    validPath = ''.join(c for c in badString if not (c in reservedCharacters)).rstrip()

    reservedNames = ('COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3',
                     'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9')

    if (validPath in reservedNames) or not (validPath):  # if the resulting path is reserved or blank path
        return findPathName(path=path, prefix=prefix)  # we generate a path name

    return validPath


def dlTrack(album, albumTitle, numberTrack, path):
    base1 = 'http://www.milesofmusik.com/'
    base2 = 'sites/default/files/tracks/'

    track = album[numberTrack]

    url = base1 + base2 + track['track_path']
    filePath = path + track['track_title'] + '.mp3'

    try:
        downloadFile(url, filePath)
        print('    successfully downloaded - ', numberTrack, track['title'])
    except:
        print("    can't download - ", numberTrack, track['title'])
        silentremove(filePath)

    else:
        # correction des id3
        try:
            meta = EasyID3(filePath)
        except mutagen.id3.ID3NoHeaderError:  # si il n'y a pas de tag id3
            meta = mutagen.File(filePath, easy=True)
            meta.add_tags()

        meta['tracknumber'] = str(numberTrack)
        meta['title'] = track['title']
        meta['album'] = albumTitle

        meta.save()


def main(url, p0=None, threads=8):
    album, albumTitle = getAlbum(url)
    print(' ', albumTitle)

    # on prepare le nom d'alb pour la creation du dossier
    p1 = convertToValidPath(albumTitle, path=p0, prefix='Album')

    path = p1 if (p0 is None) else makePath((p0, p1))

    # creation du dossier
    if not os.path.exists(path):
        os.makedirs(path)

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        for numberTrack in sorted(album.keys()):
            executor.submit(dlTrack, album, albumTitle, numberTrack, path)


if __name__ == '__main__':
    siteALB = 'http://www.milesofmusik.com/music-tracks/872884-15/1458162'
    main(siteALB)
