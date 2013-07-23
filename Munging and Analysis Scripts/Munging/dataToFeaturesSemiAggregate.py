"""
Author: Bhushan Ramnani
Created On: Monday, July 22, 2013
Description: Purpose of this script is to take the raw data from keystroke_events_final and calculate semiaggregated features from it. 
The processed data and the calculated features are inserted back into the database in the table semiAggregatedFeatures
There are 24 features: 1 unigram, 6 bigram and 15 trigram features. The last feature is just the number of times backspace or delete is pressed.
Unigram Feature: unigram dwell time

Bigram Features:
2G_dwell_K1: Dwell Time of the first key of Bigram
2G_dwell_K2: Dwell Time of second key of Bigram
2G_udl: Up-Down latency of  a bigram
2g_ddl: Down-down latency of a bigram
2G_uul: Up-Up latency of a bigram
2G_dul: Down up latency of a bigram

Trigram Features:
2G_dwell_K1: Dwell Time of the first key of trigram
2G_dwell_K2: Dwell Time of the second key of trigram
2G_dwell_K3: Dwell Time of the third key of trigram
3G_udl_K1_K2: Up-Down latency between first and the second keys of a trigram
3G_udl_K2_K3: Up-Down latency between second and the third keys of a trigram
3G_udl_K1_K3: Up-Down latency between first and the third keys of a trigram
3G_ddl_K1_K2: Down-down latency between first and the second keys of a trigram
3G_ddl_K2_K3: Down-down latency between second and the third keys of a trigram
3G_ddl_K1_K3: Down-down latency between first and the third keys of a trigram
3G_uul_K1_K2: Up-Up latency between first and the second keys of a trigram
3G_uul_K2_K3: Up-Up latency between second and the third keys of a trigram
3G_uul_K1_K3: Up-Up latency between first and the third keys of a trigram
3G_dul_K1_K2: Down-Up latency between first and the second keys of a trigram
3G_dul_K2_K3: Down-Up latency between second and the third keys of a trigram
3G_dul_K1_K3: Down-Up latency between first and the third keys of a trigram
"""

import MySqlDB as mdb


query = "select * from keystroke_events_final limit 20;"
try:
    con = mdb.connect(host="PL09-McKinley",port=3310,user="Bhushan",passwd="changeme",db="bhushan")
    cur = con.cursor()
    cur.execute(query)
    rows = cur.fetchall()
except mdb.Error, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)
finally:            
    if con:    
        con.close()

for row in rows:
    print row