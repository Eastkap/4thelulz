#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 09:11:32 2017

@author: Jacobo
"""

"""

https://s3-eu-west-1.amazonaws.com/sj-event-prod/1289/1505530416-121038.jpg
"""
from bs4 import BeautifulSoup
import requests
import os

if __name__ == '__main__':
    url = "http://www.josepho.fr/g/1289/"
    hdr = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/55.0.2883.95 Safari/537.36'}
    #session = requests.session()
    page=requests.get(url, headers=hdr)
    soup = BeautifulSoup(page.text, 'html.parser')
    #print(soup)
    for o in soup.findAll("img", {'class': 'lazyload'}):
        #print(o)
        id=str(o)[-24:-3]
        data='https://s3-eu-west-1.amazonaws.com/sj-event-prod/1289/'+id
        f = open(id,'wb')
        f.write(requests.get(data).content)
        f.close()
        #print(data)
        #os.system('wget '+data)