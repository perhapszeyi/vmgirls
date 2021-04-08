import requests
from bs4 import BeautifulSoup
import random
import linecache
from concurrent.futures import ThreadPoolExecutor
import os
import base64

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'referer':'https://www.vmgirls.com/'
}

list_title = []
list_link = []

def get_first(map_url):    
    first_website = requests.get(map_url,headers=headers)
    soup = BeautifulSoup(first_website.text,'lxml')
    label_a = soup.select('#content > ul > li > a')
    for i in label_a:
        list_title.append(i['title'])
        list_link.append(i['href'])
    get_pic()

def get_pic():
    for j in range(len(list_link)):
        pic_url = 'https://www.vmgirls.com/{page}'.format(page=list_link[j])
        pic_req = requests.get(pic_url,headers=headers)
        soup = BeautifulSoup(pic_req.text,'lxml')
        real_pic = soup.select('div.nc-light-gallery > a > img')

        for z in range(len(real_pic)):
            if not os.path.exists(list_title[j]):
                os.mkdir(list_title[j])

            images_url = "https:" + real_pic[z]['src']
            times = images_url.split('/')[-1].split('.')[0]
            suffix = images_url.split('/')[-1].split('.')[-1]
            get_images = requests.get(url=images_url,headers=headers).content
        
            with open(list_title[j]+'/'+times+'.'+suffix,'wb') as f:
                f.write(get_images)
                print('正在爬取"{name}"的第{num}张图片'.format(name=list_title[j],num=z+1))
        print('任务{num}已完成'.format(num=j+1))
        print('网址{website}'.format(website=pic_url))
        print('---------------------------------------------------------------------------------------')


if __name__ == '__main__':
    map_url = 'https://www.vmgirls.com/sitemap.html'
    get_first(map_url)