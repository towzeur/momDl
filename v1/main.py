from Album import scrapAlbum
from ArtistLibrary import scrapArtistLibrary
from Utilities import dlTrack
from cnst import *

# multitasking
import concurrent.futures

import os


def main(url, location, threads):
    ALBS = scrapArtistLibrary(url)  # we get data of the artist's albums

    for ALB in ALBS[0:3]:

        print(ALB["albName"])
        albData = scrapAlbum(BASE + ALB["albLink"])  # we get data from the alb

        fileNames = []
        for (i, trackName) in enumerate(albData['tracklist']):  # we loop into each track
            fileName = FILENAMETEMPLATE.format(ALB["artistCode"],
                                               ALB["albCode"],
                                               i + 1,
                                               trackName)
            fileNames.append(fileName)

        folder = "{}/{}/".format(ALB["artistCode"],
                                 ALB["albCode"])
        path = location + folder

        # if there are no folder we create them
        if not (os.path.exists(path)): os.makedirs(path)


        # init the multi tasking for speeding up the dl
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:

            futures = [executor.submit(dlTrack,  # function to be called
                                       FILEURL + folder + fileName,  # url of the track
                                       path,
                                       fileName) for fileName in fileNames]

            for future in concurrent.futures.as_completed(futures):
                try:
                    out = future.result()
                except Exception as exc:
                    raise (exc)
                else:
                    print(out) # i.e. » NINJAR-025_02 Pitch Black.mp3

        print()


if __name__ == "__main__":
    location = r'../MUSIC/'
    workers = 8

    url = "http://milesofmusik.com/music_catalog/library-791431/"  # ninja
    # url = "http://milesofmusik.com/music_catalog/library-155367/"  # 1-Revolution
    # url = "http://milesofmusik.com/music_catalog/library-802187/" # Chronicles of Hip Hop

    main(url, location, workers)
