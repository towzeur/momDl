import os
import requests


def silentremove(path):
    try:
        os.remove(path)
    except OSError as e:  # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occurred


def downloadFile(url, path):
    r = requests.get(url, stream=True)
    with open(path, 'wb') as f:  # we write into the file
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


def dlTrack(url, path, fileName):
    '''Download the mp3 from the link source and save it to the path location'''

    out = ""

    # Now we'll test if the file is already here so we can skip the dl
    if os.path.exists(path + fileName):
        out += '  » '

    else:  # we dl it
        try:
            downloadFile(url, path + fileName)
            out += '  ✓ '
        except:
            out += '  ✕ '
            silentremove(path + fileName)

    return out + fileName


''' eventualy we can change the id3 here
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

    meta.save()'''

if __name__ == "__main__":

    location = r'../MUSIC/'
    fileName = "025/NINJAR-025_01 Nova Prospekt.mp3"
    folder = "NINJAR/024/"

    p = location + folder
    print(p)

    if not os.path.exists(p):
        os.makedirs(p)
