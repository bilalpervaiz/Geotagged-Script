#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flickrapi import FlickrAPI
from urllib.request import urlretrieve
import os, time, sys
import json
import pandas as pd
import calendar
from io import StringIO

## API Key and secret of Flickr
key = "48949af65a962aee1b1c460d76cf09481"
secret = "secretd985cd408c7c2cfb1"
# Span to access the flickr server
wait_time = 1
## output file name
output_json = 'Etosha_flickr_photos'
keyword = sys.argv[1]
photos = []
l = 0
##Loop start
n= [1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3]
for y in [2019,2020,2021,2022,2023,2024]: ## 5 years. 

    for k in [1,1,1,2,2,2,3,3,3,4,4,4,5,5,5,6,6,6,7,7,7,8,8,8,9,9,9,10,10,10,11,11,11,12,12,12]:
        m = k
        l = l+1
        print(l)
        
        days = calendar.monthrange(y,m)[1]
        
        if n[l-1] == 3:
            min_taken_date = str(y) + '-' + str(m) + '-21'
            max_taken_date = str(y) + '-' + str(m) + '-' + str(days)
            #reset I for the next year
            if m == 12:
                l = 0
        elif n[l-1] ==2:
            min_taken_date = str(y) + '-' + str(m) + '-11'
            max_taken_date = str(y) + '-' + str(m) + '-20'
        elif n[l-1] ==1:
            min_taken_date = str(y) + '-' + str(m) + '-01'
            max_taken_date = str(y) + '-' + str(m) + '-10'
            
        print(n[l-1])
        print(min_taken_date)
        print(max_taken_date)
        
        # connecting to Flickr
        flickr = FlickrAPI(key, secret, format='parsed-json')
        
        i = 1
        while True:
            result = flickr.photos.search(
                # title = 'Etosha National Park',  #keyword 
                per_page = 700,            #number of data per page
                has_geo = 1,               #Photo that has geo location
                min_taken_date = min_taken_date, 
                max_taken_date = max_taken_date,
                bbox = '14.38637,-19.48699,17.20872,-18.38120',
 #Bounding Box of study area in the order. LonLL, LatLL, LonUR, LatUR
                media = 'photos',         # collecting photos without video
                sort =  'date-taken-desc',       # collecting photos from latest
                privacy_filter =1,
                safe_search = 1,          #  photos without violence
                extras = 'geo,url_n,date_taken,views, license, description',
                page = i
            )

            # export result
            #photos = ChainMap(photos, result['photos'])
            #photos = result['photos']
            j = result['photos']
            
            print('total_photo', j['total'])
            print('Current_pages', i)
            
            photos += j[ 'photo']

            #4000 photos can be access in one query.
            if i > 10 :
                print('Your query has been exceeded the limit of photos.4000 photos' + str(i))
                break
            elif i >= j['pages'] :
                break
            i += 1
            
# export as Json format
d = json.dumps(photos, sort_keys = True, indent = 2)
#print(d)
fp = open(output_json+str(y)+'.json', 'w' )
fp.write( d )
fp.close()
string_io = StringIO(d)

# export as csv
df = pd.read_json (string_io)
df.to_csv(output_json+str(y)+'.csv', encoding='utf-8')


# In[ ]:




