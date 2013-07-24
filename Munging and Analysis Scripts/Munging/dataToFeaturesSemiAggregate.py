"""
Author: Bhushan Ramnani
Created On: Monday, July 22, 2013
Description: Purpose of this script is to take the raw data from keystroke_events_final and calculate semiaggregated features from it. 
The processed data and the calculated features are inserted back into the database in the table semiAggregatedFeatures
There are 24 features: 1 unigram, 6 bigram and 15 trigram features. The last feature is just the number of times backspace or delete is pressed.
Unigram Feature:
unigram_dwell: unigram dwell time

Bigram Features:
bigram_dwell_K1: Dwell Time of the first key of Bigram
bigram_dwell_K2: Dwell Time of second key of Bigram
bigram_udl: Up-Down latency of  a bigram
bigram_ddl: Down-down latency of a bigram
bigram_uul: Up-Up latency of a bigram
bigram_dul: Down up latency of a bigram

Trigram Features:
trigram_dwell_K1: Dwell Time of the first key of trigram
trigram_dwell_K2: Dwell Time of the second key of trigram
trigram_dwell_K3: Dwell Time of the third key of trigram
trigram_udl_K1_K2: Up-Down latency between first and the second keys of a trigram
trigram_udl_K2_K3: Up-Down latency between second and the third keys of a trigram
trigram_udl_K1_K3: Up-Down latency between first and the third keys of a trigram
trigram_ddl_K1_K2: Down-down latency between first and the second keys of a trigram
trigram_ddl_K2_K3: Down-down latency between second and the third keys of a trigram
trigram_ddl_K1_K3: Down-down latency between first and the third keys of a trigram
trigram_uul_K1_K2: Up-Up latency between first and the second keys of a trigram
trigram_uul_K2_K3: Up-Up latency between second and the third keys of a trigram
trigram_uul_K1_K3: Up-Up latency between first and the third keys of a trigram
trigram_dul_K1_K2: Down-Up latency between first and the second keys of a trigram
trigram_dul_K2_K3: Down-Up latency between second and the third keys of a trigram
trigram_dul_K1_K3: Down-Up latency between first and the third keys of a trigram
"""



import MySQLdb as mdb
import numpy as np


#Initialize Feature Lists
unigram_dwell = []
bigram_dwell_K1 = []
bigram_dwell_K2 = []
bigram_udl = []
bigram_ddl = []
bigram_uul = []
bigram_dul = []
trigram_dwell_K1 = []
trigram_dwell_K2 = []
trigram_dwell_K3 = []
trigram_udl_K1_K2 = []
trigram_udl_K2_K3 = []
trigram_udl_K1_K3 = []
trigram_ddl_K1_K2 = []
trigram_ddl_K2_K3 = []
trigram_ddl_K1_K3 = []
trigram_uul_K1_K2 = []
trigram_uul_K2_K3 = []
trigram_uul_K1_K3 = []
trigram_dul_K1_K2 = []
trigram_dul_K2_K3 = []
trigram_dul_K1_K3 = []


def initializeFeatureLists():
    """Initializes feature lists"""
    unigram_dwell = []
    bigram_dwell_K1 = []
    bigram_dwell_K2 = []
    bigram_udl = []
    bigram_ddl = []
    bigram_uul = []
    bigram_dul = []
    trigram_dwell_K1 = []
    trigram_dwell_K2 = []
    trigram_dwell_K3 = []
    trigram_udl_K1_K2 = []
    trigram_udl_K2_K3 = []
    trigram_udl_K1_K3 = []
    trigram_ddl_K1_K2 = []
    trigram_ddl_K2_K3 = []
    trigram_ddl_K1_K3 = []
    trigram_uul_K1_K2 = []
    trigram_uul_K2_K3 = []
    trigram_uul_K1_K3 = []
    trigram_dul_K1_K2 = []
    trigram_dul_K2_K3 = []
    trigram_dul_K1_K3 = []




query = "select * from keystroke_events_final"


#Initialize Database Connection and import data
con = mdb.connect(host="PL09-McKinley",port=3310,user="Bhushan",passwd="changeme",db="bhushan")
cur = con.cursor()
cur.execute(query)
rows = cur.fetchall()


previousTurnId = rows[0][4]
bigram = 0 #It can only take values 0,1,2.
trigram1 = 0 #It can only take values 0,1,2,3
trigram2 = -1 #It can only take values 0,1,2,3
numberOfBackspaces = 0


for row in rows:
    turnId = row[4]
    if turnId!=previousTurnId:
        #Its a new turn
        #Insert Turn data into the table semi_aggregate_features

        #Remove extra features from the feature lists that come by mistake at the end of the turn
        assert(bigram==1)
        garbage = bigram_dwell_K1.pop()

        assert(trigram2==1 or trigram2==2)
        if trigram2==1:
            assert(trigram1 == 2)
        elif trigram2==2:
            assert(trigram1 == 1)
        garbage = trigram_dwell_K1.pop()
        garbage = trigram_dwell_K1.pop()
        garbage = trigram_dwell_K2.pop()
        garbage = trigram_udl_K1_K2.pop()
        garbage = trigram_ddl_K1_K2.pop()
        garbage = trigram_uul_K1_K2.pop()
        garbage = trigram_dul_K1_K2.pop()    
        
        cur.execute("INSERT INTO `semi_aggregate_features` (`turnId`,`fileName`,`userName`,`text`,`categories`,`unigram_dwell`,`bigram_dwell_K1`,`bigram_dwell_K2`,`bigram_udl`,`bigram_ddl`,`bigram_uul`,`bigram_dul`,`trigram_dwell_K1`,`trigram_dwell_K2`,`trigram_dwell_K3`,`trigram_udl_K1_K2`,`trigram_udl_K2_K3`,`trigram_udl_K1_K3`,`trigram_ddl_K1_K2`,`trigram_ddl_K2_K3`,`trigram_ddl_K1_K3`,`trigram_uul_K1_K2`,`trigram_uul_K2_K3`,`trigram_uul_K1_K3`,`trigram_dul_K1_K2`,`trigram_dul_K2_K3`,`trigram_dul_K1_K3`,`numberOfBackspaces`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(previousTurnId,row[2],row[3],row[20],row[17],np.mean(unigram_dwell),np.mean(bigram_dwell_K1),np.mean(bigram_dwell_K2),np.mean(bigram_udl),np.mean(bigram_ddl),np.mean(bigram_uul),np.mean(bigram_dul),np.mean(trigram_dwell_K1),np.mean(trigram_dwell_K2),np.mean(trigram_dwell_K3),np.mean(trigram_udl_K1_K2),np.mean(trigram_udl_K2_K3),np.mean(trigram_udl_K1_K3),np.mean(trigram_ddl_K1_K2),np.mean(trigram_ddl_K2_K3),np.mean(trigram_ddl_K1_K3),np.mean(trigram_uul_K1_K2),np.mean(trigram_uul_K2_K3),np.mean(trigram_uul_K1_K3),np.mean(trigram_dul_K1_K2),np.mean(trigram_dul_K2_K3),np.mean(trigram_dul_K1_K3),numberOfBackspaces))
        initializeFeatureLists()
        bigram = 0
        trigram1 = 0
        trigram2 = -1
        numberOfBackspaces = 0
        previousTurnId = turnId
        
    keycode = row[19]
    if keycode =='8' or keycode == '127':
        numberOfBackspaces += 1
    bigram += 1
    trigram1 += 1
    trigram2 += 1
    dwell = float(row[9])
    ddl   = float(row[10])
    udl   = float(row[11])
    unigram_dwell.append(dwell)

    if bigram == 1:
        #The only time u come here is when the new turn begins
        bigram_dwell_K1.append(dwell)
        bigramK1PressedTime = float(row[7])
        bigramK1ReleaseTime = float(row[5])
    elif bigram == 2:
        bigramK2PressedTime = float(row[7])
        bigramK2ReleaseTime = float(row[5])
        uul = bigramK2ReleaseTime - bigramK1ReleaseTime
        dul = bigramK2ReleaseTime - bigramK1PressedTime
        
        bigram_dwell_K2.append(dwell)
        bigram_udl.append(udl)
        bigram_ddl.append(ddl)
        bigram_uul.append(uul)
        bigram_dul.append(dul)
        
        bigram = 1
        bigram_dwell_K1.append(dwell)
        bigramK1PressedTime = float(row[7])
        bigramK1ReleaseTime = float(row[5])

    if trigram1 == 1:
        trigram1K1PressedTime = float(row[7])
        trigram1K1ReleaseTime = float(row[5])
        trigram_dwell_K1.append(dwell)
    elif trigram1 == 2:
        trigram1K2PressedTime = float(row[7])
        trigram1K2ReleaseTime = float(row[5])
        uul = trigram1K2ReleaseTime - trigram1K1ReleaseTime
        dul = trigram1K2ReleaseTime - trigram1K1PressedTime
        trigram_dwell_K2.append(dwell)
        trigram_udl_K1_K2.append(udl)
        trigram_ddl_K1_K2.append(ddl)
        trigram_uul_K1_K2.append(uul)
        trigram_dul_K1_K2.append(dul)
        
    elif trigram1 == 3:
        trigram1K3PressedTime = float(row[7])
        trigram1K3ReleaseTime = float(row[5])

        uul_k2_k3 = trigram1K3ReleaseTime - trigram1K2ReleaseTime
        uul_k1_k3 = trigram1K3ReleaseTime - trigram1K1ReleaseTime
        dul_k2_k3 = trigram1K3ReleaseTime - trigram1K2PressedTime
        dul_k1_k3 = trigram1K3ReleaseTime - trigram1K1PressedTime
        udl_k1_k3 = trigram1K3PressedTime - trigram1K1ReleaseTime
        ddl_k1_k3 = trigram1K3PressedTime - trigram1K1PressedTime
        
        
        trigram_dwell_K3.append(dwell)
        trigram_udl_K2_K3.append(udl)
        trigram_ddl_K2_K3.append(ddl)
        trigram_udl_K1_K3.append(udl_k1_k3)
        trigram_ddl_K1_K3.append(ddl_k1_k3)
        trigram_uul_K2_K3.append(uul_k2_k3)
        trigram_uul_K1_K3.append(uul_k1_k3)
        trigram_dul_K2_K3.append(dul_k2_k3)
        trigram_dul_K1_K3.append(dul_k1_k3)
        
        trigram1 = 1
        trigram_dwell_K1.append(dwell)
        trigram1K1PressedTime = float(row[7])
        trigram1K1ReleaseTime = float(row[5])
        
    if trigram2 == 1:
        trigram2K1PressedTime = float(row[7])
        trigram2K1ReleaseTime = float(row[5])
        trigram_dwell_K1.append(dwell)
    elif trigram2 == 2:
        trigram2K2PressedTime = float(row[7])
        trigram2K2ReleaseTime = float(row[5])
        uul = trigram2K2ReleaseTime - trigram2K1ReleaseTime
        dul = trigram2K2ReleaseTime - trigram2K1PressedTime
        trigram_dwell_K2.append(dwell)
        trigram_udl_K1_K2.append(udl)
        trigram_ddl_K1_K2.append(ddl)
        trigram_uul_K1_K2.append(uul)
        trigram_dul_K1_K2.append(dul)
        
    elif trigram2 == 3:
        trigram2K3PressedTime = float(row[7])
        trigram2K3ReleaseTime = float(row[5])

        uul_k2_k3 = trigram2K3ReleaseTime - trigram2K2ReleaseTime
        uul_k1_k3 = trigram2K3ReleaseTime - trigram2K1ReleaseTime
        dul_k2_k3 = trigram2K3ReleaseTime - trigram2K2PressedTime
        dul_k1_k3 = trigram2K3ReleaseTime - trigram2K1PressedTime
        udl_k1_k3 = trigram2K3PressedTime - trigram2K1ReleaseTime
        ddl_k1_k3 = trigram2K3PressedTime - trigram2K1PressedTime
        
        trigram_dwell_K3.append(dwell)
        trigram_udl_K2_K3.append(udl)
        trigram_ddl_K2_K3.append(ddl)
        trigram_udl_K1_K3.append(udl_k1_k3)
        trigram_ddl_K1_K3.append(ddl_k1_k3)
        trigram_uul_K2_K3.append(uul_k2_k3)
        trigram_uul_K1_K3.append(uul_k1_k3)
        trigram_dul_K2_K3.append(dul_k2_k3)
        trigram_dul_K1_K3.append(dul_k1_k3)
        
        trigram2 = 1
        trigram_dwell_K1.append(dwell)
        trigram2K1PressedTime = float(row[7])
        trigram2K1ReleaseTime = float(row[5])


#Inserting the final turn data
cur.execute("INSERT INTO `semi_aggregate_features` (`turnId`,`fileName`,`userName`,`text`,`categories`,`unigram_dwell`,`bigram_dwell_K1`,`bigram_dwell_K2`,`bigram_udl`,`bigram_ddl`,`bigram_uul`,`bigram_dul`,`trigram_dwell_K1`,`trigram_dwell_K2`,`trigram_dwell_K3`,`trigram_udl_K1_K2`,`trigram_udl_K2_K3`,`trigram_udl_K1_K3`,`trigram_ddl_K1_K2`,`trigram_ddl_K2_K3`,`trigram_ddl_K1_K3`,`trigram_uul_K1_K2`,`trigram_uul_K2_K3`,`trigram_uul_K1_K3`,`trigram_dul_K1_K2`,`trigram_dul_K2_K3`,`trigram_dul_K1_K3`,`numberOfBackspaces`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(previousTurnId,row[2],row[3],row[20],row[17],np.mean(unigram_dwell),np.mean(bigram_dwell_K1),np.mean(bigram_dwell_K2),np.mean(bigram_udl),np.mean(bigram_ddl),np.mean(bigram_uul),np.mean(bigram_dul),np.mean(trigram_dwell_K1),np.mean(trigram_dwell_K2),np.mean(trigram_dwell_K3),np.mean(trigram_udl_K1_K2),np.mean(trigram_udl_K2_K3),np.mean(trigram_udl_K1_K3),np.mean(trigram_ddl_K1_K2),np.mean(trigram_ddl_K2_K3),np.mean(trigram_ddl_K1_K3),np.mean(trigram_uul_K1_K2),np.mean(trigram_uul_K2_K3),np.mean(trigram_uul_K1_K3),np.mean(trigram_dul_K1_K2),np.mean(trigram_dul_K2_K3),np.mean(trigram_dul_K1_K3),numberOfBackspaces))




