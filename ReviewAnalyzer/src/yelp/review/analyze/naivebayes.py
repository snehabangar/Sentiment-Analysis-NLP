'''
Created on Nov 29, 2016

@author: sneha
'''
import math
import operator

class NaiveBayes:
    'Class for Naive Bayes'
    #class variable
    label = ('neg', 'neu', 'pos')
    
    def __init__(self, df):
        #initialize member variables
        self.processed_words = list(df.index.values) #word list from data frame
        [self.class_probabilities,self.words_per_class] = self.cal_class_prob(df) #calculate class probabilities
        self.labels = self.class_probabilities.keys() #set class labels
               

    def cal_class_prob(self,df):
        self.df = df 
        class_prob ={self.label[0]: 0, self.label[1]: 0,self.label[2]:0}
        words_class= {self.label[0]:df[self.label[0]].sum(), self.label[1]: df[self.label[1]].sum(), self.label[2]: df[self.label[2]].sum()}
        total = df[self.label[0]].sum() + df[self.label[1]].sum() + df[self.label[2]].sum()
        class_prob[self.label[0]] = df[self.label[0]].sum()/total
        class_prob[self.label[1]] = df[self.label[1]].sum()/total
        class_prob[self.label[2]] = df[self.label[2]].sum()/total
        return [class_prob,words_class]     
        
    def naivebayes_classify(self,review): #review text
        class_prob = {} #dictionary
        docWordCount = len(review)        
        for label in self.labels: # for each lable pos,neg,neu
            
            # logP(C) - nlog(Vc)
            prob = math.log(self.class_probabilities[label],2) - docWordCount * math.log(self.words_per_class[label],2)
            
            #calculate log(sumP(di|C))
            for word in review:
                if word in self.processed_words: #check if word is there in training data list of words
                    occurence = self.df.loc[word][label]
                    if occurence > 0:
                        prob += math.log(occurence,2) 
                    else:                      
                        prob += math.log(1,2) #laplace smoothing
                else:
                    prob += math.log(1,2) #laplace smoothing
            class_prob[label] = prob
        sorted_result = sorted(class_prob.items(), key=operator.itemgetter(1)) #sort in ascending order
        predicted_class = sorted_result[-1][0] # [label][value] -1 in array , goes to end so get max value class 
        return predicted_class    