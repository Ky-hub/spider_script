from common import *
import requests as r
import re
import json
from pyquery import PyQuery as pq
import time
host_url = 'https://www.bilibili.com/'
search_url = 'https://search.bilibili.com/all?keyword=花样滑冰&page='


def validateTitle(title):
    rstr = r'[^\u4e00-\u9fa5]'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title


if __name__ == '__main__':
    for i in range(50):
        host_page = get_response(search_url+str(i+1))
        # host_page.encoding = 'utf-8'
        document = pq(host_page.text)
        print(search_url+str(i+1))
        if i ==0:
            li_s = document("#all-list > div.flow-loader > div.mixin-list > ul.video-list.clearfix > li")
        else:
            li_s = document("#all-list > div.flow-loader > ul > li")

        for li in li_s:
            li = pq(li)
            href = li('div > div.headline.clearfix > a').attr('href')
            name =  li('div > div.headline.clearfix > a').attr('title')
            video_url = 'https:'+href
            name = validateTitle(name)
            print(name)
            print(video_url)
            mkdir(name)
            cmd = "you-get --playlist \""+video_url+"\" " + '--output-dir ' + os.path.join('.',name)
            print(cmd)
            os.system(cmd)    #有些下载会出错


            #all-list > div.flow-loader > ul > li:nth-child(1) > div > div.headline.clearfix > a

            #all-list > div.flow-loader > div.mixin-list > ul.video-list.clearfix > li:nth-child(1) > div > div.headline.clearfix > a




