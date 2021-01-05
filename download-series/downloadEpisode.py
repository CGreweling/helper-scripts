import json, sys, requests, re, os, xml
from requests.auth import HTTPBasicAuth
from xml.etree import ElementTree
from xml.dom import minidom
from shlex import quote

import config


seriesName = sys.argv[2]
episodeId = sys.argv[1]

archiveRequest = config.archiveserver + config.archiveendpoint + episodeId
sourceAuth = HTTPBasicAuth(config.sourceuser, config.sourcepassword)


def getMediapackageDataFromArchive():
    archiveResult = requests.get(archiveRequest, auth=sourceAuth, verify=False)
    archiveResult = ElementTree.fromstring(archiveResult.content)

    return archiveResult


# download catalogs with curl
def downloadCatalogs(mediapackageArchive, downloadFolder):
    for catalog in mediapackageArchive.findall(
            '{http://mediapackage.opencastproject.org}metadata/{http://mediapackage.opencastproject.org}catalog'):

        urlFromMp = catalog.find('{http://mediapackage.opencastproject.org}url').text
        filename = str(urlFromMp.split("/")[-1])

        # DownloadFile
        command = "curl -u " + config.sourceuser + ":" + config.sourcepassword + " " + urlFromMp + " -o " + downloadFolder + filename
        print(command)
        os.system(command)


# download attachments with curl
def downloadAttachments(mediapackageArchive, downloadFolder):
    for attechment in mediapackageArchive.findall(
            '{http://mediapackage.opencastproject.org}attachments/{http://mediapackage.opencastproject.org}attachment'):

        urlFromMp = attechment.find('{http://mediapackage.opencastproject.org}url').text
        filename = str(urlFromMp.split("/")[-1])

        # DownloadFile
        command = "curl -u " + config.sourceuser + ":" + config.sourcepassword + " " + urlFromMp + " -o " + downloadFolder + filename
        print(command)
        os.system(command)


def downloadTracks(mediapackageArchive, downloadFolder):
    for track in mediapackageArchive.findall(
            '{http://mediapackage.opencastproject.org}media/{http://mediapackage.opencastproject.org}track'):
        urlFromMp = track.find('{http://mediapackage.opencastproject.org}url').text
        filename = str(urlFromMp.split("/")[-1])

        # DownloadFile
        command = "curl -u " + config.sourceuser + ":" + config.sourcepassword + " " + urlFromMp + " -o " + downloadFolder + filename
        print(command)
        os.system(command)


def prettifyxml(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def createDownloadFolder(mediapackageArchive):
    title = mediapackageArchive.find('{http://mediapackage.opencastproject.org}title').text
    folder = config.targetfolder + "/" + seriesName + "/" + str(title) + "/"
    print("creating folder " + config.targetfolder + folder)
    command = "mkdir " + quote(folder)
    os.system(command)
    return quote(folder)


def main():
    mediapackageArchive = getMediapackageDataFromArchive()
    print(prettifyxml(mediapackageArchive))
    downloadFolder = createDownloadFolder(mediapackageArchive)
    downloadTracks(mediapackageArchive, downloadFolder)
    downloadAttachments(mediapackageArchive, downloadFolder)
    downloadCatalogs(mediapackageArchive, downloadFolder)


if __name__ == "__main__":
    main()
