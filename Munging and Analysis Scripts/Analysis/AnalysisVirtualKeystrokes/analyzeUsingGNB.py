'''
Created on Jun 28, 2013

@author: Bhushan Ramnani
Extracts the data from database and analyzes the data using GNB implemented for virtual keystroke classification.
'''


import MySQLdb as mdb
import sys
import keystrokeNaiveBayes
import numpy as np
import aggregatedAnalysis as aa
from sklearn import cross_validation
from scipy import interp
import pylab as pl


labelsList = ["QUESTION", "AGREE_CANDIDATE", "AGREEMENT", "EXPLANATION_CONTRIBUTION", "POSITIVITY", "GIVING_OPINION", "PREDICTION_CONTRIBUTION","HELP_REQUEST","REVOICABLE","DISAGREEMENT","CHALLENGE_CONTRIBUTION","EXPLANATION_REQUEST"]

def dataFromLabel(category):
    """Function to extract the virtual keystroke data from the database(virtual_keystrokes_view). 
    Requires: category for which the data is requied.
    Returns data,target,exampleCounts,metadata
            data: numpy array of data with shape (number_of_training_examples,). Each example is a list of rows where each row is a row from virtual_keystroke_view
            target: numpy array of data with shape (number_of_training_examples,). Each element is the integer value of the target
            exampleCounts: dictionary that contains details about number of positive,number of negative and total number of examples
            metadata: numpy array of shape (number_of_examples,2). stores turnId and username in the 0th and the 1st column respectively """
    
    try:
        con = mdb.connect(host="PL09-McKinley",port=3310)
        cur = con.cursor()
        cur.execute("CALL sp_generateData_VirtualKeystrokes_GNB('"+category+"')")
        rows = cur.fetchall()
        turns = {}
        for row in rows:
            turnId = row[4]
            
            if turnId not in turns:
                turns[turnId] = [row]
            else:
                examples = turns[turnId]
                examples.append(row)
                turns[turnId] = examples
                
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
        
    finally:            
        if con:    
            con.close()
    
    
    number_of_records = len(turns)
    metadata = np.empty((number_of_records,2),dtype = object) #stores turn id and username in the 0th and the 1st column respectively
    data = np.empty((number_of_records,),dtype=object)
    target = np.empty((number_of_records,),dtype=int)
    exampleCounts = {}
    exampleCounts["Number_of_positives"] = 0
    exampleCounts["Number_of_negatives"] = 0
    exampleCounts["Total_number_of_examples"] = number_of_records
    
    i = 0
    for eg in turns.values():
        username = eg[0][3]
        turnId = eg[0][4]
        metadata[i] = [turnId,username]
        category = eg[0][11]
        data[i]= eg
        if category == "NEGATIVE_EXAMPLE":
            target[i] = 0
            exampleCounts["Number_of_negatives"] += 1 
        else:
            target[i] = 1
            exampleCounts["Number_of_positives"] += 1 
        i += 1

    return (data,target,exampleCounts,metadata)
    

def classifyAll():
    """Classifies for all labes available in labelsList"""
    
    f = open("analysisResults.txt", "r+")
    f.write("Label\tMean Accuracy\tAUC\tZStatistic\tNumber_Of_Positives\tNumber_Of_Negatives\tTotal\n")
    
    for label in labelsList:
        (data,target,exampleCounts,metadata) = dataFromLabel(label)
        #collecting all training data in rows    
        knb = keystrokeNaiveBayes.keystrokeGNB()
        kfold = cross_validation.StratifiedKFold(target, n_folds=4)
        #kfold = cross_validation.KFold(len(data), n_folds=3)
        auc = aa.generateROCCurveAndReturnAUC(metadata,label,knb,data,target,kfold,generateCurve = True)
        zStatistic = aa.calculateZStatistic(auc,label,data,target,kfold)
        #accuracy = [gnb.fit(data[train], target[train]).score(data[test], target[test]) for train, test in kfold]
        f.write(label+"\t"+str(0.0)+"\t"+str(auc)+"\t"+str(zStatistic)+"\t"+str(exampleCounts["Number_of_positives"])+"\t"+str(exampleCounts["Number_of_negatives"])+"\t"+str(exampleCounts["Total_number_of_examples"])+"\n")
    #print cross_validation.cross_val_score(gnb, data, target, cv=kfold)
    f.close()





def classifyLabel(label):
    """Classifies only for the label passed as the parameter"""
    f = open("analysisResults.txt", "r+")
    f.write("Label\tMean Accuracy\tAUC\tZStatistic\tNumber_Of_Positives\tNumber_Of_Negatives\tTotal\n")
    (data,target,exampleCounts,metadata) = dataFromLabel(label)
    #collecting all training data in rows    
    knb = keystrokeNaiveBayes.keystrokeGNB()
    kfold = cross_validation.StratifiedKFold(target, n_folds=4)
    #kfold = cross_validation.KFold(len(data), n_folds=3)
    auc = aa.generateROCCurveAndReturnAUC(metadata,label,knb,data,target,kfold,generateCurve = True)
    zStatistic = aa.calculateZStatistic(auc,label,data,target,kfold)
    #accuracy = [gnb.fit(data[train], target[train]).score(data[test], target[test]) for train, test in kfold]
    f.write(label+"\t"+str(0.0)+"\t"+str(auc)+"\t"+str(zStatistic)+"\t"+str(exampleCounts["Number_of_positives"])+"\t"+str(exampleCounts["Number_of_negatives"])+"\t"+str(exampleCounts["Total_number_of_examples"])+"\n")
    f.close()








def classifyAllUsingConfusionMatrix():
    """Classifies for all labes available in labelsList"""
    
    f = open("analysisResults2.txt", "r+")
    f.write("Label\tMean Accuracy\tAUC\tZStatistic\tNumber_Of_Positives\tNumber_Of_Negatives\tTotal\n")
    
    for label in labelsList:
        (data,target,exampleCounts,metadata) = dataFromLabel(label)
        #collecting all training data in rows    
        knb = keystrokeNaiveBayes.keystrokeGNB()
        kfold = cross_validation.StratifiedKFold(target, n_folds=4)
        #kfold = cross_validation.KFold(len(data), n_folds=3)
        (tp,fp,tn,fn) = aa.classifyAndReturnConfusionMatrix(metadata,knb,data,target,kfold)
        #accuracy = [gnb.fit(data[train], target[train]).score(data[test], target[test]) for train, test in kfold]
        f.write(label+"\t"+str(tp)+"\t"+str(fp)+"\t"+str(tn)+"\t"+str(fn)+"\t"+str(exampleCounts["Number_of_positives"])+"\t"+str(exampleCounts["Number_of_negatives"])+"\t"+str(exampleCounts["Total_number_of_examples"])+"\n")
    #print cross_validation.cross_val_score(gnb, data, target, cv=kfold)
    f.close()
    
    
    




def classifyLabelUsingConfusionMatrix(label):
    f = open("analysisResults.txt", "r+")
    f.write("Label\tTP\tFP\tTN\tFN\tNumber_Of_Positives\tNumber_Of_Negatives\tTotal\n")
    (data,target,exampleCounts,metadata) = dataFromLabel(label)
    #collecting all training data in rows    
    knb = keystrokeNaiveBayes.keystrokeGNB()
    kfold = cross_validation.StratifiedKFold(target, n_folds=4)
    (tp,fp,tn,fn) = aa.classifyAndReturnConfusionMatrix(metadata,knb,data,target,kfold)
    #accuracy = [gnb.fit(data[train], target[train]).score(data[test], target[test]) for train, test in kfold]
    f.write(label+"\t"+str(tp)+"\t"+str(fp)+"\t"+str(tn)+"\t"+str(fn)+"\t"+str(exampleCounts["Number_of_positives"])+"\t"+str(exampleCounts["Number_of_negatives"])+"\t"+str(exampleCounts["Total_number_of_examples"])+"\n")
    f.close()


classifyAll()


if __name__ == '__main__':
    pass
