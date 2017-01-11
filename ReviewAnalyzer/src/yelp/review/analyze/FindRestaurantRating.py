'''
Created on Dec 1, 2016

@author: sneha
'''

import pandas as pd
import json
import review
from yelp.review.analyze.review import readReviews, readNgramWords, \
    create_training_df, tokenize
from yelp.review.analyze.naivebayes import NaiveBayes

traing_count = 500
testcount = 100

def readSpecificResReviews(fileName, businessId):    
    data = []
    with open(fileName) as f:
        for line in f:
            data.append(json.loads(line))
    review = []   
    for line in data:
        if line['business_id'] ==businessId:    
            review.append({'text':line['text'],'stars':line['stars']})                  
    return review  
       

if __name__ == '__main__':
    #yelp_review_dataset_file = './../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_restaurant_review.json'
    #yelp_review_dataset_file = './../yelp_dataset_challenge_academic_dataset/PANERA_BREAD_review.json'
    yelp_review_dataset_file = './../yelp_dataset_challenge_academic_dataset/PF_CHANG_review.json'
    

    restaurant = []  
    #restaurant.append(["OZfpG8tDCcIEq8pzgZdyKw","Applebee's"])
    #restaurant.append(["FiXamVMgMf9U0VqFHDZSEA","Panera Bread"])
    restaurant.append(["JDDeaNfb0JXD1NbznSIC9g", "P.F. Chang's"])
    training_set_pos = readReviews('./../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_restaurant_review_pos.json', 0,traing_count)
    training_set_neu = readReviews('./../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_restaurant_review_neu.json', 0,traing_count)
    training_set_neg = readReviews('./../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_restaurant_review_neg.json', 0,traing_count)
    ngram_words = readNgramWords('./../yelp_dataset_challenge_academic_dataset/ngram_words.txt')
  
    #BOW_df = createBOW(training_set, ngram_words)
    training_set = training_set_pos
    for neu in training_set_neu:
        training_set.append(neu)
    for neg in training_set_neg:
        training_set.append(neg)        
    
    
    df = create_training_df(training_set, ngram_words)
    nb = NaiveBayes(df)    
    result = []
    for res in restaurant:
        review_set = readSpecificResReviews(yelp_review_dataset_file,res[0])
        document = tokenize(review_set,ngram_words)
        i = 0            
        pos = 0
        neg = 0
        neu = 0   
        for review in document:
            review_class = nb.naivebayes_classify(review)
            if review_class == 'neu':
                neu +=1
            elif review_class == 'pos':
                pos +=1
            else:
                neg +=1
        analysys_dict = {'neg':neg,'neu':neu,'pos':pos}                
        result.append({'restaurantname':res[1] ,'reviewcount':analysys_dict})
        i+=1
        #if(i > 50):
        #    break
pd.set_option('display.max_rows', len(df))
print result