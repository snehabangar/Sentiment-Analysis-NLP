'''
Created on Dec 1, 2016

@author: sneha Bangar
'''

import json
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

class MaxEntropy:
    'Class for Maximum Entropy'
    #class variables
    label = ('neg', 'neu', 'pos')
    stop = set(stopwords.words('english'))
    
    #tokenize review text
    def tokenize(self, review, ngram_words):        
        port = PorterStemmer()       
        splitted_text = self.split_text(review)
        #stopwords removal
        filtered_text = [word for word in splitted_text if word not in stopwords.words('english')]
        
        #apply stemming
        stemmed_text = [port.stem(word) for word in filtered_text]
        
        #apply n-gram model
        text_with_ngrams = self.generate_ngrams(stemmed_text, ngram_words)        
        return text_with_ngrams

    def expand_around_chars(self, text, characters):
        for char in characters:
            text = text.replace(char, ' '+char+' ')        
        return text
 
    def split_text(self,text):    
        text = text.replace('\n', ' ')
        text = self.expand_around_chars(text, '";.,()[]{}:;')
        splitted_text = text.split(' ')
        cleaned_text = [x for x in splitted_text if len(x)>1]
        text_lowercase = [x.lower() for x in cleaned_text]
        stop_cleaned_text = [x for x in text_lowercase if x not in self.stop]        
        return stop_cleaned_text
    #generate n-grams from review text
    def generate_ngrams(self, text, ngram_words):
        new_text = []
        index = 0
        while index < len(text):
            [new_word, new_index] = self.concatenate_words(index, text, ngram_words)
            new_text.append(new_word)
            index = new_index+1 if index!= new_index else index+1
        return new_text
    #concatenate words to generate n-gram
    def concatenate_words(self, index, text, ngram_words):
        word = text[index]
        if index == len(text)-1:
            return word, index
        if word in ngram_words:
            [word_new, new_index] = self.concatenate_words(index+1, text, ngram_words)
            word = word + ' ' + word_new
            index = new_index
        return word, index
    
    def readReviews(self,fileName,ngram_words, start, endcount):    
        data = []
        with open(fileName) as f:
            for line in f:
                data.append(json.loads(line))
        review = []
        i = 0
        for line in data:    
            if i>=start:
                if line['stars'] == 3:
                    stars = self.label[1]
                elif line['stars'] > 3:  
                    stars = self.label[2]
                else:       
                    stars = self.label[0]
                tokenize_words = self.tokenize(line['text'], ngram_words)    
                review.append([tokenize_words,stars])
            i+=1
            if i > endcount:
                break   
        return review
    
    def readNgramWords(self, fileName):    
        ngramWords = []
        with open(fileName) as f:
            for line in f:
                ngramWords = line.split(',')    
        return ngramWords
    
    def list_to_dict(self,words_list):
        return dict([(word, True) for word in words_list])   
        
    def __init__(self, filename):
        self.fileName = filename
    
    #create a maximum entropy classifier with training data    
    def createClassifier(self,training_set_formatted):
        numIterations = 3 #25 ##change to 2 for demo
        algorithm = nltk.classify.MaxentClassifier.ALGORITHMS[0] # 0 for max ent
        classifier = nltk.MaxentClassifier.train(training_set_formatted, algorithm, max_iter=numIterations) # TRAIN
        #classifier.show_most_informative_features(10)
        return classifier
    
    #apply classifier on test data
    def classifyReviews(self,test_reviews, classifier):
        result = []
        result.append('Predicted  Actual')
        for review in test_reviews:
            label = review[1] #actual class
            text = review[0]
            determined_label = classifier.classify(text) #predicted class
            result.append([determined_label, label])
        return result   
    
    #calculate accuracy
    def calculateAcc(self, result):
        correct = 0
        for row in result:
            print row
            if row[0] == row[1]:
                correct+=1                
        accuracy = correct / float(len(result)) * 100        
        return accuracy 

#create training and test datasets

traing_count = 1000 #4000#2000
testcount =  200 #1000#500    
training_filename='./../yelp_dataset_challenge_academic_dataset/review_training.json'   
test_filename='./../yelp_dataset_challenge_academic_dataset/review_test.json' 
maxEn = MaxEntropy(training_filename)  

ngram_words = maxEn.readNgramWords('./../yelp_dataset_challenge_academic_dataset/ngram_words.txt')
training_set_pos = maxEn.readReviews('./../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_restaurant_review_pos.json', ngram_words, 0,traing_count)
training_set_neu = maxEn.readReviews('./../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_restaurant_review_neu.json',ngram_words, 0,traing_count)
training_set_neg = maxEn.readReviews('./../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_restaurant_review_neg.json',ngram_words, 0,traing_count)
test_set_pos = maxEn.readReviews('./../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_restaurant_review_pos.json',ngram_words, traing_count+1,traing_count+testcount)
test_set_neu = maxEn.readReviews('./../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_restaurant_review_neu.json',ngram_words, traing_count+1,traing_count+testcount)
test_set_neg = maxEn.readReviews('./../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_restaurant_review_neg.json',ngram_words, traing_count+1,traing_count+testcount)

training_set = training_set_pos
for neu in training_set_neu:
    training_set.append(neu)
for neg in training_set_neg:
    training_set.append(neg)        

test_set = test_set_pos
for neu in test_set_neu:
    test_set.append(neu)
for neg in test_set_neg:        
    test_set.append(neg)
#convert list to dictionary as nltk needs dictionary format    
training_set_formatted = [(maxEn.list_to_dict(element[0]), element[1]) for element in training_set] 
test_set_formatted = [(maxEn.list_to_dict(element[0]), element[1]) for element in test_set]
#call maximum entropy classifier
classifier = maxEn.createClassifier(training_set_formatted)
result = maxEn.classifyReviews(test_set_formatted, classifier)
#calculate accuracy
accuracy = maxEn.calculateAcc(result)
print accuracy