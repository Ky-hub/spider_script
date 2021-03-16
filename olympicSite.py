import requests as r
import re
import json
from pyquery import PyQuery as pq
from lxml import etree
import threading
import os
from common import *

# html = etree.HTML(wb_data)
# html_data = html.xpath('/html/body/div/ul/li/a')
# json_url = "https://www.olympic.org/ajaxscript/loadmorevideos/%7B899C61A8-1851-45A1-B999-D224A1305722%7D/6/0/" 
url = "https://www.olympic.org/videos/figure-skating"
host = "https://www.olympic.org"
topic_urls = [] 
video_urls = []





def get_ts_urls(url):
    response = get_response(url)
    document = pq(response.text)
    m3u8_json_url = document('#wrapper > div.main > div > section.photo-block > section > div > a').attr('href')
    response = get_response(host+m3u8_json_url)
    content = json.loads(response.content) 
    m3u8_url = content['src']
    response = get_response(m3u8_url)
    m3u8_url = parse_url(response.text)[-1]
    response =get_response(m3u8_url)
    ts_urls = parse_url(response.text)
    return ts_urls

def angle_ts_load(path,url):
    with open(path,"wb") as fp:
        while True:
            try:
                response = r.get(url,timeout = 20)
                fp.write(response.content)
                fp.close()
                break
            except r.exceptions.ConnectionError:
                print('timeout reconncet')
            except r.exceptions.ReadTimeout:
                print('timeout reconncet')


def concat_video(video_files,name):
    cmd = "ffmpeg -i \"concat:"+'|'.join(video_files)+"\""+" "+ name+'.mp4'
    os.system(cmd)
    print(cmd)
   
def dowm_load_video(path_,urls,name):
    threads = []
    video_files = []
    number = len(urls)
    for i in range(len(urls)):
        url = urls[i]
        path = path_ + str(i+1)+'.ts'
        video_files.append(path)
        t = threading.Thread(target=angle_ts_load,args=(path,url))
        threads.append(t)

    for t in threads:
        t.setDaemon(True)
        t.start()

    for t in threads:
        t.join() 

    print('hello')
    concat_video(video_files,path_)

def get_topic():
    response = get_response(url)
    document = pq(response.text)
    ul = document('#ajax-area-68bfb93a55344d5a8708630d6c10a4d4-3fc90d13-eb8d-404b-8643-7e46dd48b208 > ul')
    a_s = ul('li>a')
    for a in a_s:
        href = pq(a).attr('href')
        topic_urls.append(host+href)
    




if __name__ == '__main__':
    get_topic()
    for topic_url in topic_urls: 
        save_urls = []
        topic = topic_url.split('/')[-1]
        mkdir(topic)
        response = get_response(topic_url)
        document = pq(response.text)
        video_li = document('#wrapper > div.main > div > section.mosaic-box.alt > div > ul > li')
        for li in video_li:
            li = pq(li)
            video_urls.append(li('span>a').attr('href'))
            save_urls.append(li('span>a').attr('href'))
        
        more_button = document('#wrapper > div.main > div > section.mosaic-box.alt > div > span > a')
        if more_button:
            more_json_url = more_button.attr('href')
            more_json = get_response(host + more_json_url)
            content = json.loads(more_json.content)['content']
            nextUrl = json.loads(more_json.content)['nextUrl']
            for li in content:
                video_urls.append(li['url'])
                save_urls.append(li['url'])
            while nextUrl:
                more_json_url = nextUrl
                more_json = get_response(host + more_json_url)
                content = json.loads(more_json.content)['content']

                for li in content:
                    video_urls.append(li['url'])
                    save_urls.append(li['url'])
        

                nextUrl = json.loads(more_json.content)['nextUrl']
        print(save_urls)
        for save_video_url in save_urls:
            name = save_video_url.split('/')[-1]
            ts_urls =  get_ts_urls(host+save_video_url)
            dowm_load_video(os.path.join(topic,name),ts_urls,name)











