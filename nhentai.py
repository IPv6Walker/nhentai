# /home/s_y/.conda/envs/nhentai/bin python
# -*- coding: utf-8 -*-

import requests
import argparse
import bs4
import sys
import re
import os

__author__ = 'Bruno'

index_path = None
parser = argparse.ArgumentParser()
parser.add_argument('--data_dir', type=str,
                    help='Directory for storing downloaded albums')
parser.add_argument('--search', type=str,
                    help='Input search string for resources in nhnetai')
index_path, unparsed = parser.parse_known_args()

root_url = 'https://nhentai.net'

if index_path.search:
    index_url = root_url + '/search/?q=' + index_path.search + '+chinese&sort=popular'
else:
    index_url = root_url

try:
    if index_path.data_dir:
        os.mkdir('/mnt/d/Y/' + index_path.data_dir + '/') # 采集 gID_aID_pNum 的文件路径
    elif index_path.search:
        index_path.data_dir = '/mnt/d/Y/' + index_path.search + '/'
        os.mkdir(index_path.data_dir)
    else:
        index_path.data_dir = '/mnt/d/Y/manga/'
        os.mkdir(index_path.data_dir)
except FileExistsError:
    pass

galleries_data_file = open(index_path.data_dir + '/' + 'galleries_data' + '.txt', 'w+') # 采集 galleries_data 的文件

def get_galleries_urls():
    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    return [a.attrs.get('href') for a in soup.select('div.gallery a[href^=/g]')]

def get_galleries_data(galleries_url):
    galleries_data = {}
    page_url = root_url + galleries_url
    response = requests.get(page_url)
    soup = bs4.BeautifulSoup(response.text,'html.parser')

    galleries_ID = u''.join(re.findall(r'/\d*/', galleries_url))
    galleries_data['galleries_ID'] =  re.sub(r'\D', "", galleries_ID) # 漫画页面ID galleries_ID

    script_code = soup.body.script.next_sibling.next_sibling.text
    albums_ID = u''.join(re.findall(r"\"media_id\":\"\d*\"", script_code))
    galleries_data['albums_ID'] = re.sub(r'\D', "", albums_ID) # 图片链接ID albums_ID

    page_Num = u''.join(soup.select('div#info')[0].contents[7].text)
    galleries_data['page_Num'] = re.sub(r'\D', "", page_Num) # 漫画页数 page_Num

    title = re.sub(r'\D\xbb\D{36}', "", u''.join(soup.select('title')[0].text)) # 漫画标题 title
    unmatchable_str = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    galleries_data['title'] = re.sub(unmatchable_str, "_", title)
    
    print(galleries_data, file=galleries_data_file) # 将每个页面的 galleris_data 输出到一个特定的文件
    return galleries_data

def get_link(m, n):
    galleries_data = get_galleries_data(m)
    range_max = int(galleries_data['page_Num']) + 1
    rename = str(n) + '-' + str(n)
    img_path = index_path.data_dir + '/' + str(n) + '/'
    os.mkdir(img_path)
    link = open(img_path + 'link.txt', 'w+')
    gID_aID_pNum = open(index_path.data_dir + '/' + rename + '.txt', 'w+')
    gID_aID_pNum.write(galleries_data['galleries_ID'] + '_' + galleries_data['albums_ID']+ '_' + galleries_data['page_Num'] + '_《' + galleries_data['title'] + '》')
    for i in range(1, range_max):
        j = "https://i.nhentai.net/galleries/" + galleries_data['albums_ID'] + "/" + '%d' %i + ".jpg" + '\n'
        p = "https://i.nhentai.net/galleries/" + galleries_data['albums_ID'] + "/" + '%d' %i + ".png" + '\n'
        print(j, file=link)
        print(p, file=link)

def show_galleries_stats():
    galleries_urls = get_galleries_urls()
    for i in range(1,len(galleries_urls)):
        get_link(galleries_urls[i],i)


show_galleries_stats()