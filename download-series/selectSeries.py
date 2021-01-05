#!/bin/python
import requests,re,os
from requests.auth import HTTPBasicAuth
import tkinter as tk
from tkinter import *
import json
import config

#Digest login source server
sourceauth = HTTPBasicAuth(config.sourceuser, config.sourcepassword)

seriesDiconary = dict()

#get Series count
archiveSeriesCount = "/series/count"
archiveSeriesCountrequest = config.archiveserver + archiveSeriesCount
print(archiveSeriesCountrequest)
seriesCount = requests.get(archiveSeriesCountrequest, auth=sourceauth)
print(archiveSeriesCountrequest)
print(seriesCount.text + " Series found")

finalSeriesString=''

#python reqeusts can not handle as much data as e.g. firefox so... paging
page=0
#result per request
resultsize=1
seriesCount = int(seriesCount.text)
#get the number of pages
pages = seriesCount/resultsize
archiveenpoint = "/series/series.json?count="+str(resultsize)+"&startPage="+str(page)
archiverequest = config.archiveserver + "/series/series.json"
archiveresult = requests.get(archiverequest, auth=sourceauth).json()
print(archiveresult)

if archiveresult['catalogs']:
  for m in archiveresult['catalogs']:
      print(m['http://purl.org/dc/terms/']['title'][0]['value'])
      if  m['http://purl.org/dc/terms/']['identifier'][0]['value'] not in finalSeriesString:
        title=m['http://purl.org/dc/terms/']['title'][0]['value']
        seriesId=m['http://purl.org/dc/terms/']['identifier'][0]['value']
        finalSeriesString=finalSeriesString+title+ " ; "+seriesId+'\n'
        #safe id+title in an dictonary
        seriesDiconary.update({seriesId:title})

#save all Series to File seperated by ';'
f = open('All_Series_List.txt', 'w')
f.write(str(finalSeriesString.encode('UTF-8')))
f.close()

selectedSeries = dict()


def writeSelectedSeriestoFile():
    selectedSeriesFile = ''
    for key, value in selectedSeries.items():
        if value.get() == '1':
           selectedSeriesFile+=selectedSeriesFile + key+' ; ' + " " + '\n'
    f = open("Selecet_Series_File.txt",'w')
    f.write(str(selectedSeriesFile.encode('UTF-8')))
    f.close()
    print("Select_Series_File.txt Created!")


def download():
    print("download" + str(selectedSeries))
    for key, value in selectedSeries.items():
        if value.get() == '1':
            print(key)
            command = "python downloadSeries.py " + key
            os.system(command)


#create ui to select Series for download
root = tk.Tk()
vsb = tk.Scrollbar(root, orient="vertical")
text = tk.Text(root, width=40, height=20,
                            yscrollcommand=vsb.set)
vsb.config(command=text.yview)
vsb.pack(side="right", fill="y")
text.pack(side="left", fill="both", expand=True)


for key, value in seriesDiconary.items():
      selectedSeries[key] = Variable()
      checkButton = tk.Checkbutton(root, text=value+" : "+key, variable=selectedSeries[key])
      text.window_create("end", window=checkButton)
      text.insert("end", "\n") # to force one checkbox per line

button = Button(root, text='Download Selected Series', command=download)
button.pack()
button = Button(root, text="Create Selected Series File", command=writeSelectedSeriestoFile)
button.pack()
button = Button(root, text="Quit!", fg='red', command=root.destroy)
button.pack()

root.mainloop()
