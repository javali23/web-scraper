#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import csv
from collections import Counter
from string import punctuation
from nltk.corpus import stopwords


# In[2]:


def findall(soup, tagname, cls):
    tag = soup.find(tagname, class_ = cls)
    while tag is not None:
        yield tag
        tag = tag.find_next(tagname, class_ = cls)
    


# In[22]:


def extractReviews(link):
    source = requests.get(link).text
    soup   = BeautifulSoup(source, 'lxml')
    reviews = findall(soup, 'div', 'review-content')
    for review in reviews:
        try:
            rating = int(review.img['alt'][0])
            review_text = review.a.text+" " + review.p.text.strip()
            
        except Exception as e:
            review_text = review.a.text
        yield rating, review_text


# In[4]:


def sumarize(link):
    pros = Counter()
    cons = Counter()
    stop_words = set(stopwords.words('english')) 
    for rating, review in extractReviews(link):
        if rating<3:
            spl = review.split()
            cons.update(w.lower().rstrip(punctuation)  for w in spl if w  not in stop_words)
        else:
            spl = review.split()
            pros.update(w.lower().rstrip(punctuation)  for w in spl if w  not in stop_words)    
        
    
    return [y for y in pros.most_common(10)], [y for y in cons.most_common(10)]


# In[5]:


source = requests.get(r'https://www.trustpilot.com/categories/art_handicraft').text
soup   = BeautifulSoup(source, 'lxml')
shops = soup.find('div', class_='categoryBusinessListWrapper___14CgD')


# In[28]:


with open('customer_review.csv', 'w') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(['store_name', 'rating', 'pros', 'cons'])
    for shop in findall(shops, 'a', 'internal___1jK0Z wrapper___26yB4'):
        try:
            store_name = shop.find('div',class_="businessTitle___152-c").text
            rating = int(shop.find('div',class_='starRating___2Qn5z medium___1FEFm').img['alt'][-1])
            link = shop['href']
            pros, cons = sumarize(f'https://www.trustpilot.com{link}')
            csv_writer.writerow([store_name, rating, pros, cons])
        except Exception as e:
            pass


# In[ ]:




