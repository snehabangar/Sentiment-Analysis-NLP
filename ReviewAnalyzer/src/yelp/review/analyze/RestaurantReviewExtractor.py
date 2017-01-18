'''
Created on Dec 1, 2016

@author: sneha Bangar
'''

import json


fileName='./../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json'
catFile='./../yelp_dataset_challenge_academic_dataset/yelp_restaurant_category.txt'
review_filename='./../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json'
rest_review_filename='./../yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_restaurant_review.json'

data = []
categories = set()
business_id = set()
business = ""
#read category file
with open(catFile) as catf:
    for line in catf:
        categories.add(line.strip())
#read business file and get all the restaurants from businesses        
with open(fileName) as f:
    for line in f:
            data.append(json.loads(line))
    review = []
    i = 0
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
rest_count = 0
rest_review_data =""
#for all the businesses of type restaurant, retrieve reviews from review file
with open(review_filename) as f:
    for line in f:
            review_data.append(json.loads(line))
    review = []  
    for line in review_data:         
        bid = line['business_id']        
        if bid in business_id:            
            rest_review_data += json.dumps(line)
            rest_review_data +='\n'    
            rest_count +=1                                                                                 
#save the restaurant review in file       
with open(rest_review_filename, 'w') as outfile:
    outfile.write(rest_review_data)         