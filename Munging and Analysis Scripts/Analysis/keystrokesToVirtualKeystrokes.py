'''
Created on Jun 26, 2013

@author: Bhushan Ramnani
"""The script is used to transform the keystroke events dataset to a more disaggregated dataset of virtual keystrokes(digraphs and trigraphs)

'''

import MySQLdb as mdb
import sys

leftContextList = ["","X","_"]
focusList = ["X", "_"]
rightContextList = ["", "X", "_"]


try:
    con = mdb.connect(host="PL09-McKinley",port=3310,user="Bhushan",passwd="changeme",db="bhushan")
    cur = con.cursor()
    cur.execute("SELECT * from keystroke_events_final")
    rows = cur.fetchall()
    
    firstKeyOfTurn = True
    lastKeyOfTurn = False
    l = len(rows)
    
    for i in xrange(l):
        thisTurnId = rows[i][4]
        
        if i != 0:
            previousTurnId = rows[i-1][4]
        else:
            previousTurnId = "Gibberish"
           
        if i != (l-1): 
            nextTurnId = rows[i+1][4]
        else:
            nextTurnId = "Gibberish"
        
        if thisTurnId!=previousTurnId: #first key of the turn
            previousKey = "["
            previousKeyCode = "["
        else:
            previousKey = rows[i-1][16]
            previousKeyCode= rows[i-1][19]    
    
        
        if thisTurnId!=nextTurnId: #last key of the turn
            nextKey = "]"
            nextKeyCode = "]"
        else:
            nextKey = rows[i+1][16]
            nextKeyCode = rows[i+1][19]
            
        thisKey = rows[i][16]
        thisKeyCode = rows[i][19]
        
            
        for leftContext in leftContextList:
            for focus in focusList:
                for rightContext in rightContextList:
                    if leftContext == "X":
                        leftContextKey = previousKey
                        leftContextCode = previousKeyCode
                    else:
                        leftContextKey = leftContext
                        leftContextCode = leftContext
                    
                    if focus == "X":
                        focusKey = thisKey
                        focusCode = thisKeyCode
                    else:
                        focusKey = focus
                        focusCode = focus
                                        
                    if rightContext == "X":
                        rightContextKey = nextKey
                        rightContextCode = nextKeyCode
                    else:
                        rightContextKey = rightContext
                        rightContextCode = rightContext
                                            
                    cur.execute("INSERT INTO `virtual_keystrokes` (`eventId`,`keystrokeId`,`userName`,`turnId`,`dwellTime`,`downDownLatency`,`upDownLatency`,`leftContextCharacter`,`focusCharacter`,`rightContextCharacter`,`leftContextKeycode`,`focusKeycode`,`rightContextKeycode`,`numberOfTimesHeld`,`categories`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(rows[i][0],rows[i][1],rows[i][3],rows[i][4],rows[i][9],rows[i][10],rows[i][11],str(leftContextKey),str(focusKey),str(rightContextKey),str(leftContextCode),str(focusCode),str(rightContextCode),rows[i][8],rows[i][17]))
                    #print insertQuery
                    #cur.execute(insertQuery)
except mdb.Error, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)
        
finally:            
    if con:    
        con.close()

if __name__ == '__main__':
    pass