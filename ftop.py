#!/usr/bin/python3

import requests
import re
from bs4 import BeautifulSoup
import os
import sys
import argparse
from multiprocessing import Pool,Queue,Process
import multiprocessing
import time

#image_src = []
#image_timeout = []
base_url = "https://ftopx.com"
#base_url = "https://ftopx.com/tags/blowjob"
#python ftop.py -lmn "/tags/blowjob/page/" -start 1 -end 3 -output blowjob

def parser_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument('-lmn',default='/page/')
    parser.add_argument('-start',default=1,type=int)
    parser.add_argument('-end',default=10,type=int)
    parser.add_argument('-output',default="ftop")
    args = parser.parse_args()
    return args


def creat_soup(url):
    '''
    return a soup object
    :param url: a href
    '''
    response  = requests.get(url)
    #lxml or html.parser
    return BeautifulSoup(response.text,'html.parser')


def get_images_in_page(page):
    url = base_url + '/page/' + page
    soup = creat_soup(url)
    images_info = soup.find_all('div',class_='thumbnail')

    folder = 'images/'
    if os.path.exists(folder) == False:
        os.makedirs(folder)

    for img in images_info:
        # get image href
        href = "https://ftopx.com" + img.a.get('href')

        # get image of origin resolution
        origin = "https://ftopx.com" +  origin_url(href)

        image_url = get_image_url(origin)

        # save image to ./images
        save_image(folder,image_url)
        print(image_url)


def origin_url(url):
     soup = creat_soup(url)
     href = soup.find('div',class_='res-origin').a.get('href')
     return href

def get_image_url(url):
    soup = creat_soup(url)
    img = soup.find(class_ = "photo").img.get('src')
    return img

def save_image(folder,url):
    time.sleep(2)
    html = requests.get(url)
    filename = re.match(r'.*/(.*?\.jpg)',url).group(1)
    with open(folder+filename,'wb') as file:
        file.write(html.content)


if __name__ == '__main__':
    #args = parser_arg()
    get_images_in_page('1')

