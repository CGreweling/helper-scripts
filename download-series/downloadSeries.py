import sys, requests, re, os

from requests.auth import HTTPBasicAuth
from shlex import quote

import config

sourceauth = HTTPBasicAuth(config.sourceuser, config.sourcepassword)

def createSeriesFolder():
    command = "mkdir " + quote(config.targetfolder + "/" + seriesname)
    os.system(command)

def downloadEachEpisode():
    for event in searchrequest:
         print("Downloading id: " + event['identifier'] + "\n")
         command = 'python downloadEpisode.py ' + event['identifier'] + " " + quote(seriesname)
         print(command + "\n")
         os.system(command)



# get Events from for series from api
searchrurl = config.archiveserver + "/api/events?filter=is_part_of:" + sys.argv[1]
searchrequest = requests.get(searchrurl, auth=sourceauth, headers=config.header).json()
seriesname = searchrequest[0]['series']

createSeriesFolder()
downloadEachEpisode()

