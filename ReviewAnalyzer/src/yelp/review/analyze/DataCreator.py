'''
Created on Nov 26, 2016

@author: sneha Bangar
'''
import json
from operator import itemgetter

fileName='./../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json'
catFile='./../yelp_dataset_challenge_academic_dataset/yelp_restaurant_category.txt'
review_filename='/../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json'
rest_pos_review_filename='./../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_restaurant_review_pos_50k.json'
rest_neg_review_filename='./../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_restaurant_review_neg_50k.json'
rest_neu_review_filename='./../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_restaurant_review_neu_50k.json'
rest_name_filename='./../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_restaurant_name.json'
data = []
categories = set()
business_id = set()
business = ""

#read category file - this file contains all the categories related to restaurants from yelp category list 
with open(catFile) as catf:
    for line in catf:
        categories.add(line.strip())
#read business data file        
with open(fileName) as f:
    for line in f:
            data.append(json.loads(line))
    review = []
    i = 0
    #get business id and name of each business having the category mentioned in categories
    for line in data:    
        cat = line['categories']
        bid = line['business_id']
        if bid not in business_id:
            for c in cat:
                if c in categories:
                    bdetails = {'business_id':line['business_id'],'name':line['name']}
                    temp = json.dumps(bdetails)
                    business +=temp
                    business +='\n'
                    business_id.add(line['business_id'])
                    break
                    
review_data = []
rest_pos_review_data = ""
rest_neg_review_data = ""
rest_neu_review_data = ""    
rest_count = 0
#read the review file
with open(review_filename) as f:
    for line in f:
            review_data.append(json.loads(line))
    review = []
    i = 0
    neu_count = 0
    pos_count = 0
    neg_count = 0
    #retrieve reviews for each type positive,negative,neutral 
    for line in review_data:         
        bid = line['business_id']
        stars = line['stars']
        if bid in business_id:
            #reviews with rating 3 are considered neutral
            if stars == 3:
                if neu_count < 50000:
                    rest_neu_review_data += json.dumps(line)
                    rest_neu_review_data +='\n' 
                    rest_count+=1
                    neu_count+=1
            elif stars > 3: 
                #reviews with rating greater than 3 are considered positive
                if pos_count < 50000:
                    rest_pos_review_data += json.dumps(line)
                    rest_pos_review_data +='\n' 
                    rest_count+=1
                    pos_count+=1
            else:
                #reviews with rating less than 3 are considered negative
                if neg_count < 50000:
                    rest_neg_review_data += json.dumps(line)
                    rest_neg_review_data +='\n' 
                    rest_count+=1      
                    neg_count+=1                                                                        
        if rest_count > 150000:
            break
#write reviews and restaurants in separate files    
with open(rest_pos_review_filename, 'w') as outfile:
    outfile.write(rest_pos_review_data) 
with open(rest_neg_review_filename, 'w') as outfile:
    outfile.write(rest_neg_review_data) 
with open(rest_neu_review_filename, 'w') as outfile:
    outfile.write(rest_neu_review_data)               
with open(rest_name_filename, 'w') as outfile:
    outfile.write(business)          