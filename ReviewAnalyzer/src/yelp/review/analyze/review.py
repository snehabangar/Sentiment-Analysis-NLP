'''
Created on Nov 26, 2016

@author: sneha
'''
import json
import pandas as pd
from sets import Set
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer



scores = (1,2,3,4,5)
stops = set(stopwords.words("english"))
port = PorterStemmer()

#Input - file name , start count, end count
#Output - review([review_text][stars])
def readReviews(fileName, start, count):    
    data = []
    with open(fileName) as f:
        for line in f:
            data.append(json.loads(line))
    review = []
    i = 0
    for line in data:
        if i>=start:    
            review.append({'text': line['text'] , 'stars': line['stars'] }) #add dctionary to review
        i+=1        
        if i > count:
            break          
    return review

def readNgramWords(fileName):    
    ngramWords = []
    with open(fileName) as f:
        for line in f:
            ngramWords = line.split(',')    
    return ngramWords

def tokenize(test_set, ngram_words):    
    words_set = []    
    for review in test_set:
        score = review['stars']
        text = review['text']
        splitted_text = split_text(text)
        filtered_text = [word for word in splitted_text if word not in stopwords.words('english')]
        stemmed_text = [port.stem(word) for word in filtered_text]
        text_with_ngrams = generate_ngrams(stemmed_text, ngram_words)
        words_set.append(text_with_ngrams)
    return words_set
    
def expand_around_chars(text, characters):
    for char in characters:
        text = text.replace(char, ' '+char+' ')        
    return text
 
def split_text(text):    
    text = text.replace('\n', ' ')
    text = expand_around_chars(text, '";.,()[]{}:;')
    splitted_text = text.split(' ')
    cleaned_text = [x for x in splitted_text if len(x)>1]
    text_lowercase = [x.lower() for x in cleaned_text]
    return text_lowercase

def generate_ngrams(text, ngram_words):
    new_text = []
    index = 0
    while index < len(text):
        [new_word, new_index] = concatenate_words(index, text, ngram_words)
        new_text.append(new_word)
        index = new_index+1 if index!= new_index else index+1
    return new_text
 
def concatenate_words(index, text, ngram_words):
    word = text[index]
    if index == len(text)-1:
        return word, index
    if word in ngram_words:
        [word_new, new_index] = concatenate_words(index+1, text, ngram_words)
        word = word + ' ' + word_new
        index = new_index
    return word, index


def getLabel(stars):
    if stars == 3:
        label = 'neu'
    elif stars > 3:
        label = 'pos'
    else: 
        label = 'neg'
    return label        
        
def create_training_df(training_set, ngram_words):
    df = pd.DataFrame(columns=['neg','neu','pos'])
    words_set = Set()
    i = 0
    for item in training_set:
        stars = item['stars']
        label = getLabel(stars)
        text = item['text']
        splitted_text = split_text(text)
        #filtered_text = [word for word in splitted_text if word not in stopwords.words('english')]
        #stemmed_text = [port.stem(word) for word in filtered_text]
        
        #with ngrams        
        text_with_ngrams = generate_ngrams(splitted_text, ngram_words)
        
        #for word in splitted_text:   #without ngram     
        for word in text_with_ngrams:           
            if word not in words_set:
                words_set.add(word)
                df.loc[word] = [0,0,0]
                df.ix[word][label] += 1
            else:
                df.ix[word][label] += 1
        i +=1
        #if(i > 10000):
        #    break        
    return df

