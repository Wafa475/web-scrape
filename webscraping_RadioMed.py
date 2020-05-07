# -*- coding: utf-8 -*-
"""

# Web Scraping with Beautifulsoup(Radio Med)

importing the packages
"""

import requests 
import re
import csv 
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd

"""set site url"""

site = "https://radiomedtunisie.com/category/%d8%a3%d8%ae%d8%a8%d8%a7%d8%b1/" # set site url


"""define the useful part of html code"""

article = []
titles = []
types = []
i = 0
print('************************************************')
print('*********************start *********************')
print('************************************************')


    
   for j in range(10) : #we can vary the number of items scraped using this loop example here I put 10 ie I can scraped 100 items, 5 gives 50 items ect
   resultat = requests.get(site) 
   resultat.status_code
   #if status_code == 200 everything is OK
   source = resultat.text # Extracting the code HTML
   soup = BeautifulSoup(source,'html.parser') # Convert HTML to a BeautifulSoup object
   w1 = soup.find_all(class_ = 'the-next-page')
   a1 = BeautifulSoup(str(w1), "html.parser")
   a11 = a1.find('a')
   site=a11.get('href')
   w = soup.find_all(class_ = 'post-title')
   a = BeautifulSoup(str(w), "html.parser")
   links = a.find_all('a')
   # Extract all links
   relative_urls = [link.get('href') for link in links]
   full_urls = [urljoin(site, url) for url in relative_urls]

   for url in full_urls:
    
    # connect to every webpage
    page = requests.get(url)
    print('connect to {0}: {1}'.format(i+1,url))   
    # get HTML from webpage
    source1 = page.text
    
    # convert HTML to BeautifulSoup object
    soup1 = BeautifulSoup(source1, 'html.parser')
    # find articles
    content = soup1.find_all('div' , class_ = 'entry-content entry clearfix')
    ar = BeautifulSoup(str(content), "html.parser")
    artic = ar.find_all('p')
    # find titles
    title = soup1.find('h1' , class_='post-title entry-title')
    
    # find the type
    type1 = soup1.find_all('span', class_='post-cat-wrap')
    tp = BeautifulSoup(str(type1), "html.parser")
    type2 = tp.text
    # Transforming to text and cleaning every desired element in the page
    art = [(p.text).replace('\n','').replace('\t','').replace('\r','') for p in artic]
    tit = [(t.string).replace('\n','').replace('\t','').replace('\r','') for t in title]
    print('the title')
    print(tit)
    print('the type')
    print(type2)
    print('the article')
    print(art)
    
    article.append(art)
    titles.append(tit)
    types.append(type2)
    
    i = i+1
print('***********************************************************')   
print('****************************Finish*************************')
print('***********************************************************')
df = pd.DataFrame(list(zip(full_urls, titles, article, types)), columns =['link', 'titles', 'article', 'type'])
df.to_csv(r'radiomed.csv' ,encoding='utf-8-sig')

