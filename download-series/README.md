# Download All Eiposdes of Series
A series folder will be created with the name of the series
In the series folder for each episode a folder with the eipsode name is created.
In the episode folder all attachments, tracks and caralogs will be downloaded. 

## How to use it
Edit config.py 

dnf install tkinter

Run:
python select Series.py
 - Select the Series to download from the Source Server
 - Create a File(SelectedSeries) with the Selected Series 
 - Or start to Ingest the Series:
 
 All Episodes of each selected Series will be downloaded from the Source Server to local Diskstorage.

A TextFile with All Series of the Source Server will be created in this Programmfolder. 
The shema ist "SeriesName ; SeriesId" for simple Import into Excel sheet.
So a non IT-Guy can sort and select the wanted Series.

## Downloading from Commandline

To download Series from a file where a Series Id is in each line:

```for line in $(cat SelectedSeries.txt); do python downloadSeries.py $line; done```
