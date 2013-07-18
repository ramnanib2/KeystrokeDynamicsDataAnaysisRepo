'''
Created on May 29, 2013

@author: Bhushan Ramnani (bramnani@cs.cmu.edu)

Python Script to combine column annotations table and keylogs data

Usage:
python combineKeyStrokeAndColumnAnnotations <keylogfile> <columnannotationfile>
The result is saved as a separate file with the same name as the keylog file name with the suffix - Processed

Update version 2: added the ability to figure out latencies and dwell times from the time stamps
'''
import csv
import sys
import string
import random
import os


def columnAnnotationClean(fileToOpen):
    """Add a new column called category and assign value to it based on the annotated row category. Returns the cleaned file as a file object"""
    
    filenameToWrite = ''.join(random.choice(string.ascii_uppercase+string.digits) for x in range(7)) 
    filenameToWrite = filenameToWrite+".csv"
    fileToWrite = open(filenameToWrite,"wb")
    #fileToWrite.close()
    #fileToWrite = open('test4.csv',"r+")
    reader = csv.reader(fileToOpen)
    writer = csv.writer(fileToWrite)
    x = 0;
    labels = []
    for row in reader:
        category = ""
        if x==0:
            x=1
            labels = row
            header = labels[1:4]
            header.append("CATEGORIES")
            writer.writerow(header)
            continue
        for i in xrange(4, len(row)):
            if row[i]=='1':
                if category == '':
                    category = labels[i]
                else:
                    category = category+','+labels[i]
        row = row[1:4]#
        row.append(category)
        writer.writerow(row)

    fileToWrite.close()
    return filenameToWrite



def collectKeystrokeData(keyStrokeReader):
    """A csv reader file keyStrokeReader. Returns two lists. header: consists of header row as a list; keyStokeData: list of keystroke data rows"""
    header = [] #header for the final file
    keyStrokeRows = [] #list of all keystroke rows
    flag = False
    isFirstEvent = False
    lastPressedTimeStamp = {}
    lastReleasedTimeStamp = 0.0
    lastPressed = 0.0

    i = 1
    for row in keyStrokeReader:
        if i <=2:
            i = i+1
            continue
        if i==3:
            header = ["FILE_NAME"]+row+["DWELL_TIME","DD_LATENCY","UD_LATENCY"]
            i = i+ 1
            continue
        if row[1] == "sync" and flag==False:
            lastReleasedTimeStamp = 0.0
            isFirstEvent = True
            flag = not(flag)
            snippet = []
            continue
		
		
		#Adding down down latency and up down latency
        if row[1] == "pressed" and isFirstEvent == False:
            keycode = row[3]
            lastPressedTimeStamp[keycode] = float(row[0])
		
            ddl = float(row[0]) - lastPressed
            if lastReleasedTimeStamp == 0.0:
                udl = 0.0
            else:
                udl = float(row[0]) - lastReleasedTimeStamp
            lastPressed = float(row[0])
            row = row + ["0.0", str(ddl),str(udl)]
		
		#Adding dwell time
        if row[1] == "release" and isFirstEvent == False:
            keycode = row[3]
            lastReleasedTimeStamp = float(row[0])
            dwellTime = lastReleasedTimeStamp - lastPressedTimeStamp[keycode]
            row = row + [str(dwellTime), "0.0", "0.0"]
		
        if row[1] == "pressed" and isFirstEvent == True:
            row = row + ["0.0", "0.0", "0.0"]
            isFirstEvent = False
            keycode = row[3]
            lastPressedTimeStamp[keycode] = float(row[0])
            lastPressed = float(row[0])

			
        if row[1] == "sync" and flag==True:
            isFirstEvent = True
            isAvalidKey = False
            lastReleasedTimeStamp = 0.0
            for x in snippet:
                if x[3] not in ("8", "10", "16", "32"):
                    isAvalidKey = True
                    break
            if isAvalidKey:
                for x in snippet:
                    keyStrokeRows.append(x)
                keyStrokeRows.append(row)
            snippet = []
            continue 
        if flag:
            snippet.append(row)
            
    return header, keyStrokeRows


def collectColumnAnnotatedData(columnAnnotatedReader, file):
    """A csv reader file columnAnnotatedReader. Returns two lists. header: consists of header row as a list; columnAnnotatedRows: list of columnAnnotated data rows"""
    header = columnAnnotatedReader.next()
    header = ["TURN_ID"]+header
    columnAnnotatedRows = []
    i=1
    for row in columnAnnotatedReader:
        if row[0] == "TUT" or row[1]=="":
            continue
        turnId = "Turn_"+str(i)+"_"+file
        i = i+1
        row = [turnId]+row
        columnAnnotatedRows.append(row)

    return header,columnAnnotatedRows
        


def writeToFinalFile(writer,header,header2,keyStrokeRows,columnAnnotatedRows, processedFileName):
    
    writer.writerow(header+[header2[0]]+header2[2:len(header2)])   
    i = -1
      
    for row2 in columnAnnotatedRows:
        
        i = i+1
        if i>=len(keyStrokeRows):
                break
        row = keyStrokeRows[i]
        transcriptTimeStamp = float(row2[-2])
#        if row[1]=="sync":
#            keylogTimestamp = float(row[0])
#            i = i+1
#            if i>=len(keyStrokeRows):
#                break
#            row = keyStrokeRows[i]
            
        rowsToWrite = []
        while (row[1]!="sync"):
            rowToWrite = [processedFileName]+row+[row2[0]]+row2[2:(len(row2))]
            rowsToWrite.append(rowToWrite)
            i = i+1
            if i>=len(keyStrokeRows):
                break
            row = keyStrokeRows[i]
            if row[1]=="sync":
                keylogTimeStamp = float(row[0])
                if abs(transcriptTimeStamp-keylogTimeStamp) <= 5000.0:
                    for x in rowsToWrite:
                        writer.writerow(x)
                else:
                    i = i+1
                    if i>=len(keyStrokeRows):
                        break
                    row = keyStrokeRows[i]
                    rowsToWrite = []
    
        
        
#        rowToWrite = [processedFileName]+row+row2[1:(len(row2))]
#        writer.writerow(rowToWrite)
#        i = i+1
#        row = keyStrokeRows[i]
#        while row2[0] == row[len(row)-1]: #while the usernames are the same
#            rowToWrite = [processedFileName]+row+row2[1:(len(row2))]
#            writer.writerow(rowToWrite)
#            
        
    

def main():
    keyStrokeData = open(sys.argv[1])#open("bios13a02-2013-03-11-0929-48.tsv")#
    columnAnnotatedData = open(sys.argv[2])#open("bios13a02_message_annotations.csv")#
    keyStrokeReader = csv.reader(keyStrokeData, delimiter='\t')
    filenameToWrite = columnAnnotationClean(columnAnnotatedData) #clean the columnannotated data
    columnAnnotatedDataClean = open(filenameToWrite)
    columnAnnotatedReader = csv.reader(columnAnnotatedDataClean)
    keyLogFileName = sys.argv[1]#"RandomFileNamr1234"#
    processedFileName = keyLogFileName[0:(len(keyLogFileName)-4)]+"_Processed.csv"
    fileToWrite = open(processedFileName,"wb")
    writer = csv.writer(fileToWrite)
    
    
    #collect all the keystroke data
    header, keyStrokeRows = collectKeystrokeData(keyStrokeReader)
    

    #collect all column annotated data
    file = sys.argv[2]
    file = file[0:9]
    header2, columnAnnotatedRows = collectColumnAnnotatedData(columnAnnotatedReader, file)
    
    writeToFinalFile(writer,header,header2,keyStrokeRows,columnAnnotatedRows,processedFileName)
    columnAnnotatedDataClean.close()
    os.remove(filenameToWrite)
            
    
#    for row in keyStrokeReader:
#        if i <=2:
#            i = i+1
#            continue
#        if i==3:
#            row2 = columnAnnotatedReader.next()
#            header = ["FILE_NAME"]+row+row2[1:len(row2)]
#            writer.writerow(header)
#            i = i+1
#            continue
#        if row[1] == "sync":
#            flag2 = not(flag2)
#            continue
#        
#        
#        if flag2:
#            row2 = columnAnnotatedReader.next()
#            while row2[0] != row[len(row)-1]: #while the usernames do not match
#                row2 = columnAnnotatedReader.next() #iterate until the usernames match
#            flag2 = not(flag2)
#            
#        rowToWrite = [processedFileName]+row+row2[1:(len(row2))]
#        writer.writerow(rowToWrite)
        
#        if j ==200:
#            break
#        print row
#        j = j+ 1
        
try:
    main()
except StopIteration:
    print "Make sure the keylog file and the column annotated files are in sync"

if __name__ == '__main__':
    pass