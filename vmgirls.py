from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import random
import linecache
import os
import base64
import timeit


headers = {
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
}

vmgirls_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'referer':'https://www.vmgirls.com/'
}

Proxy_pool = []
list_title = []
list_link = []

def pool():
    for i in range(1,11):
        agent_url = 'https://www.kuaidaili.com/free/inha/{page}/'.format(page=i)
        ans = requests.get(agent_url,headers=headers)
        soup = BeautifulSoup(ans.text,'lxml')
        ip = soup.select('td[data-title="IP"]')
        port = soup.select('td[data-title="PORT"]')
        for i,p in zip(ip,port):
            url = 'https://www.baidu.com/'
            agent = i.text + ':' + p.text
            proxies = {'http': agent}
            ans = requests.get(url,proxies=proxies)
            if ans.status_code == 200:
                Proxy_pool.append(agent)
            else:
                pass

def get_first(map_url):
    first_website = requests.get(map_url,headers=vmgirls_headers)
    soup = BeautifulSoup(first_website.text,'lxml')
    label_a = soup.select('#content > ul > li > a')
    for i in label_a:
        list_title.append(i['title'])
        list_link.append(i['href'])
    get_pic()

def get_pic():
    for j in range(len(list_link)):
        random_ip = random.choice(Proxy_pool)
        proxies_ip = {'http': random_ip}
        # print(proxies_ip)
        s = timeit.default_timer()
        pic_url = 'https://www.vmgirls.com/{page}'.format(page=list_link[j])
        pic_req = requests.get(pic_url,headers=vmgirls_headers,proxies=proxies_ip)
        soup = BeautifulSoup(pic_req.text,'lxml')

        div = soup.find_all('div',class_='nc-light-gallery')

        for z in div:
            if not os.path.exists(list_title[j]):
                os.mkdir(list_title[j])

            images = z.find_all('img')
            for x in tqdm(range(len(images))):
                images_url = "https:" + images[x]['src']
                try:
                    requests.get(images_url,headers=vmgirls_headers,proxies=proxies_ip)
                    times = images_url.split('/')[-1].split('.')[0]
                    suffix = images_url.split('/')[-1].split('.')[-1]
                    get_images = requests.get(url=images_url,headers=vmgirls_headers,proxies=proxies_ip).content
            
                    with open(list_title[j]+'/'+times+'.'+suffix,'wb') as f:
                        f.write(get_images)
                except:
                    pass
        print('任务{num}已完成'.format(num=j+1))
        print('网址{website}'.format(website=pic_url))
        e = timeit.default_timer()
        print('运行时间为：',e-s,'秒')
        print('---------------------------------------------------------------------------------------')

if __name__ == '__main__':
    pool()
    map_url = 'https://www.vmgirls.com/sitemap.html'
    get_first(map_url)
