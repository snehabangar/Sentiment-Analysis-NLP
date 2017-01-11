'''
Created on Nov 27, 2016

@author: sneha
'''
import pandas as pd
import review
from yelp.review.analyze.review import readReviews, readNgramWords, \
    create_training_df, tokenize
from yelp.review.analyze.naivebayes import NaiveBayes

trainig_count = 1000
testcount = 200

if __name__ == '__main__':
    training_set_pos = readReviews('./../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_restaurant_review_pos.json', 0,trainig_count)
    training_set_neu = readReviews('./../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_restaurant_review_neu.json', 0,trainig_count)
    training_set_neg = readReviews('./../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_restaurant_review_neg.json', 0,trainig_count)
    ngram_words = readNgramWords('./../yelp_dataset_challenge_academic_dataset/ngram_words.txt')

    test_set_pos = readReviews('./../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_restaurant_review_pos.json', trainig_count+1,trainig_count+testcount)
    test_set_neu = readReviews('./../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_restaurant_review_neu.json', trainig_count+1,trainig_count+testcount)
    test_set_neg = readReviews('./../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_restaurant_review_neg.json', trainig_count+1,trainig_count+testcount)
  
    #BOW_df = createBOW(training_set, ngram_words)
    #combine pos + neu + neg training set
    training_set = training_set_pos
    for neu in training_set_neu:
        training_set.append(neu)
    for neg in training_set_neg:
        training_set.append(neg)        
    
     #combine pos + neu + neg test set
    test_set = test_set_pos
    for neu in test_set_neu:
        test_set.append(neu)
    for neg in test_set_neg:        
        test_set.append(neg)
    
    #create training data  data frame
    df = create_training_df(training_set, ngram_words)
    nb = NaiveBayes(df)    
    document = tokenize(test_set,ngram_words) #list of tokenized review text
    i = 0
    analysys_dict = dict.fromkeys(['predicted_class','stars','text'])
    result = []
    for review in document:
        review_class = nb.naivebayes_classify(review)
        analysys = dict({'predicted_class': review_class, 'stars': test_set[i]['stars'], 'text':test_set[i]['text']})
        result.append(analysys)
        i+=1
        #if(i > 50):
        #    break
#pd.set_option('display.max_rows', len(df))
correct = 0      
for res in result:  
    print res['predicted_class'] + ' ' + str(res['stars']) + ' ' + res['text']   
    if res['stars'] == 3:
        stars = 'neu'
    elif res['stars'] > 3:  
        stars = 'pos'
    else:       
        stars = 'neg'
    if res['predicted_class'] == stars:
        correct+=1                
accuracy = correct / float(len(result)) * 100        
print accuracy 