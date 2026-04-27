import json
import re
import csv

fileExtension = ".eqp"
inputFileName = f"Arknights Armor (by location)"
csvExtension = ".csv"
outputFileName = f"{inputFileName} Documentation{csvExtension}"
csvText = [
    ['Location','Material','DR','TL','Cost','Weight','Flexible','Holdout','Don time','Vulnerability']
]

with open(f"{inputFileName}{fileExtension}") as file:
    gurpsAkArmor = json.load(file)

for location in gurpsAkArmor['rows']:
    for material in location['modifiers']:
        if(material['name'] != '@Covers only half (front only, one arm, etc)@'):
            localNotesList = []
            for item in material['local_notes'].split(';'):
                localNotesList.append(item.lstrip())
                if(item == ''):
                    localNotesList.pop()
            
            dr = ''
            flex = 'No'
            holdout = ''
            dontime = ''
            vulnerable = 'N/A'

            for note in localNotesList:
                if(re.search("DR\s\d", note )):
                    dr = re.sub('[^\d\-\+]','',note)
                if(re.search("Flexible",note)):
                    flex = "Yes"
                if(re.search("Holdout",note)):
                    holdout = re.sub('[^\d\-\+]','',note)
                if(re.search("Don\stime",note)):
                    dontime = re.sub('[^\d\-\+]','',note)
                if(re.search("crushing",note)):
                    vulnerable = note

            csvText.append([location['description'],material['name'],dr,material['tech_level'],material['cost'],material['weight'],flex,holdout,dontime,vulnerable])

with open(outputFileName, 'w', newline='') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(csvText)
