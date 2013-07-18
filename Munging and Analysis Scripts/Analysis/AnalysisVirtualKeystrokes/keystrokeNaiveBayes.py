'''
Created on Jun 28, 2013

@author: Bhushan Ramnani

Implementation of Gaussian Naive Bayes algorithm for mental state classification using disaggregated virtual keystroke model. Contains classify and learn functions
'''

import numpy as np
import math


class keystrokeGNB:
    """Gaussian Naive Bayes implementation for keystroke data analysis"""
    
    classProbability = {} #store the probability for a particular class
    keystrokeMeanAndStdDev = {} #store (mean,stdDev) tuple for a particular keystroke feature
    vocabulary = set() #vocabulary of keystrokes
    
    def __init__(self):
        self.Probability = {}
        self.keystrokeMeanAndStdDev = {}
        self.vocabulary = set()
    
    def cleanFeatures(self,virtualKeycode,dwell,ddl,udl):
        """Takes the keycode and returns feature names to be considered. Feature names are 'none' if they are not to be considered"""
        #in the virtualKeycode, if the first character,second character and the last character are all spaces, then it's a unigram, dont consider ddl and udl. Only consider the dwell time
        #if the first and the second characters are spaces, but the last character is not a space, then its a bigram with no left context, so do not consider ddl and udl. only consider the dwell time yo !!
        #if the first keycode is [, then also don't consider ddl and udl, only consider dwell
        #if both the ddl and udl are zero then also do not consider the keystroke
        if (virtualKeycode[0]==" " and virtualKeycode[1]==" ") or virtualKeycode[0]=="[" or (ddl==0.0 and udl==0.0):
            dwellFeatureName = virtualKeycode+"{dwell}"
            ddlFeatureName = None
            udlFeatureName = None
        else:
            dwellFeatureName = virtualKeycode+"{dwell}"
            ddlFeatureName = virtualKeycode+"{ddl}"
            udlFeatureName = virtualKeycode+"{udl}"
        
        return (dwellFeatureName,ddlFeatureName,udlFeatureName)

    
    def updateCounts(self,eg):
        """Takes a turn which is basically a list of rows from virtual_keystroke_view belonging to a particular turn"""
        """Updates the keystrokeMeanAndStdDev Dictionary"""
        for row in eg:
            virtualKeycode = row[9]
            category = row[11]
            if category=="NEGATIVE_EXAMPLE":
                category = "negative"
            else:
                category = "positive"
            dwell = float(row[5])
            ddl = float(row[6])
            udl = float(row[7])
            
            dwellFeatureName,ddlFeatureName,udlFeatureName = self.cleanFeatures(virtualKeycode, dwell,ddl,udl)
            
            if dwellFeatureName is not  None:
                if (dwellFeatureName,category) in self.keystrokeMeanAndStdDev:
                    A = self.keystrokeMeanAndStdDev[(dwellFeatureName,category)]
                    A.append(dwell)
                    self.keystrokeMeanAndStdDev[(dwellFeatureName,category)] = A
                else:
                    self.keystrokeMeanAndStdDev[(dwellFeatureName,category)] = [dwell]
            
            if ddlFeatureName is not None:        
                if (ddlFeatureName,category) in self.keystrokeMeanAndStdDev:
                    A = self.keystrokeMeanAndStdDev[(ddlFeatureName,category)]
                    A.append(ddl)
                    self.keystrokeMeanAndStdDev[(ddlFeatureName,category)] = A
                else:
                    self.keystrokeMeanAndStdDev[(ddlFeatureName,category)] = [ddl]
            
            if udlFeatureName is not None:
                if (udlFeatureName,category) in self.keystrokeMeanAndStdDev:
                    A = self.keystrokeMeanAndStdDev[(udlFeatureName,category)]
                    A.append(udl)
                    self.keystrokeMeanAndStdDev[(udlFeatureName,category)] = A
                else:
                    self.keystrokeMeanAndStdDev[(udlFeatureName,category)] = [udl]      
    
    
    def calculateKeystrokeMeanAndStdDevFromCount(self):
        garbageFeatures = []
        for feature in self.keystrokeMeanAndStdDev:
            A = self.keystrokeMeanAndStdDev[feature]
            l = len(A)
            if l < 300 or l > 8000: #excluding features with too less samples
                garbageFeatures.append(feature)
                continue
            avg = np.mean(A)
            stdDev = np.std(A)
            self.keystrokeMeanAndStdDev[feature] = (avg,stdDev)
        for f in garbageFeatures:#removing features with too less number of samples
            garbage = self.keystrokeMeanAndStdDev.pop(f)
            
    
    
    def fit(self,trainingExamples, target):
        """Requires a list of training examples. Each training example corresponds to a turn ID. Each training example is a list of rows from that turn which is the key. These rows come from virtual_keystroke_view"""
        """Learns the class probabilities as well as the P(feature|class)"""
        """trains the GNB classifier and returns the object"""
        
        total = len(target)
        positiveCount = np.sum(target)
        negativeCount = total-positiveCount
        
        for eg in trainingExamples:            
            self.updateCounts(eg)
            
        total = positiveCount + negativeCount
        self.classProbability["positive"] = positiveCount/total
        self.classProbability["negative"] = negativeCount/total
        self.calculateKeystrokeMeanAndStdDevFromCount()
        print "Training Complete"
        return self
        
    
    def calculateGaussianProbability(self,x,meanAndStd):
        mean,std = meanAndStd
        #print "mean=",mean,"  std=",std
        #if std==0:
        #    return 1.0
        temp = (math.pow((x-mean),2))/(2*math.pi*std*std)
        temp2 = math.exp(-temp)
        answer = (temp2/(math.sqrt(2*math.pi*std*std)))
        if answer==0:
            return 1.0
        else:
            return answer
    


    
    def reInitializeObjectProperties(self):
        """Reinitializes object properties to respective empty values"""
        self.classProbability = {} #store the probability for a particular class
        self.keystrokeMeanAndStdDev = {} #store (mean,stdDev) tuple for a particular keystroke feature
        self.vocabulary = set() #vocabulary of keystrokes



        
    def predict_proba(self,testExamples):
        """Requires a numpy array of training examples. Each training example corresponds to a turn ID. Each training example is a list of rows from that turn which is the key. These rows come from virtual_keystroke_view"""
        """Returns a 2D numpy array (num_of_examples*number of classes) of probabilities"""
        
        num_examples = len(testExamples)
        probas = np.empty((num_examples,2))
        
        i = 0
        for eg in testExamples:
            positiveProb = 0.0
            negativeProb = 0.0
            for row in eg:
                virtualKeycode = row[9]
                dwell = float(row[5])
                ddl = float(row[6])
                udl = float(row[7])
                
                dwellFeatureName, ddlFeatureName, udlFeatureName  = self.cleanFeatures(virtualKeycode, dwell, ddl, udl)
                
                if dwellFeatureName is not None:
                    if ((dwellFeatureName,"positive")) in self.keystrokeMeanAndStdDev:
                        positiveProb += math.log(self.calculateGaussianProbability(dwell,self.keystrokeMeanAndStdDev[(dwellFeatureName,"positive")]))
                    elif ((dwellFeatureName,"negative")) in self.keystrokeMeanAndStdDev:
                        negativeProb += math.log(self.calculateGaussianProbability(dwell,self.keystrokeMeanAndStdDev[(dwellFeatureName,"negative")]))
                
                if ddlFeatureName is not None:
                    if ((ddlFeatureName,"positive")) in self.keystrokeMeanAndStdDev:
                        positiveProb += math.log(self.calculateGaussianProbability(ddl,self.keystrokeMeanAndStdDev[(ddlFeatureName,"positive")]))
                    elif ((ddlFeatureName,"negative")) in self.keystrokeMeanAndStdDev:
                        negativeProb += math.log(self.calculateGaussianProbability(ddl,self.keystrokeMeanAndStdDev[(ddlFeatureName,"negative")]))
                
                if udlFeatureName is not None:
                    if ((udlFeatureName,"positive")) in self.keystrokeMeanAndStdDev:
                        positiveProb += math.log(self.calculateGaussianProbability(udl,self.keystrokeMeanAndStdDev[(udlFeatureName,"positive")]))
                    elif ((udlFeatureName,"negative")) in self.keystrokeMeanAndStdDev:
                        negativeProb += math.log(self.calculateGaussianProbability(udl,self.keystrokeMeanAndStdDev[(udlFeatureName,"negative")]))
            
            positiveProb += self.classProbability["positive"]
            negativeProb += self.classProbability["negative"]

            
            probas[i] = [negativeProb,positiveProb]
            i+=1
        
        self.reInitializeObjectProperties()
        return probas
                




    def predict(self,testExamples):
        """Requires a numpy array of shape (number_of_examples,) thats in the virtual keystroke data format"""
        """Returns a list of binary predictions"""
        
        predictions = []
        probas = self.predict_proba(testExamples)
        
        for i in xrange(len(probas)):
            if probas[i][0] > probas[i][1]:
                predictions.append(0)
            else:
                predictions.append(1)
        
        return predictions                
        
        