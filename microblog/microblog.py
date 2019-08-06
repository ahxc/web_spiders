from urllib.parse import urlencode
from pyquery import PyQuery as pq

import requests

base_url = 'https://m.weibo.cn/api/container/getIndex?'

headers = {
        'Host': 'm.weibo.cn',
        'Referer': 'https://m.weibo.cn/u/2830678474',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) '\
        +'AppleWebKit/537.36 (KHTML, like Gecko) '\
        +'Chrome/58.0.3029.110 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        }

def get_page(page):
    params = {
        'type': 'uid',
        'value': '2834256503',
        'containerid': '1076032834256503',
        'page': page
        }
    url = base_url + urlencode(params)  

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()

    except requests.ConnectionError as e:
        print('Error', e.args)

def parse_page(json):
    if json:
        items = json.get('data').get('cards')
        for item in items:
            item = item.get('mblog')
            weibo = {}
            weibo['id'] = item.get('id')
            weibo['text'] = pq(item.get('text')).text()# 初始化并获得其文本
            weibo['reposts'] = item.get('reposts_count')
            weibo['comments'] = item.get('comments_count')
            weibo['attitudes'] = item.get('attitudes_count')

            if item.get('pics') is not None:
                pics = item.get('pics')
                pics_list = []
                for pic in pics:
                    pics_list.append(pic.get('url'))

                weibo['pics'] = pics_list

            yield weibo

def sava_pics(result):
    for i, url in enumerate(result['pics']):
        img = requests.get(url)
        with open(result['id']+'-{}.jpg'.format(i), 'wb') as f:
            f.write(img.content)

if __name__ == '__main__':
    for page in range(1, 11):
        json = get_page(page)
        results = parse_page(json)
        for result in results:
            print(result)

            if 'pics' in result:
                sava_pics(result)