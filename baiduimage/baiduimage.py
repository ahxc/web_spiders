from urllib.parse import urlencode, quote, unquote

import requests
import re
import urllib
import json

def get_page(keyword, page):
    keyword = quote(keyword)

    headers = {
    'Host': 'image.baidu.com',
    'Referer': 'http://image.baidu.com/search/index?tn=baiduimage&fm=result&ie=utf-8&word={}'.format(keyword),
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) '\
    +'AppleWebKit/537.36 (KHTML, like Gecko) '\
    +'Chrome/58.0.3029.110 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    }
    
    keyword = unquote(keyword)

    params = {   
               'tn': 'resultjson_com',
               'ipn': 'rj',
               'ct': '201326592',
               'fp': 'result',
               'queryWord': keyword,
               'cl': '2',
               'lm': '-1',
               'ie': 'utf-8',
               'oe': 'utf-8',
               'st': '-1',
               'ic': '0',
               'word': keyword,
               'face': '0',
               'istype': '2',
               'nc': '1',
               'pn': page,
               'rn': '30',
               'gsm': '1e'
    }

    url = 'https://image.baidu.com/search/index?'+urlencode(params)
    #print(url)

    try:
        response = requests.get(url, headers=headers)

        return response.json()

    except Exception as e:
        print(e)
        return None


def parse_page(json):
    #print(json)
    if json.get('data'):
        for item in json.get('data'):
            if item.get('middleURL'):

                image_url = item.get('middleURL')
            #print(image_url)
                yield{
                'url': image_url
                }


def save_pics(items, page):
    for i, item in enumerate(items):
        with open('items.txt', 'a', encoding='utf-8') as f:
            f.write(json.dumps(item['url'], ensure_ascii=False)+'\n')

        with open(str(page)+'-'+str(i)+'.jpg', 'ab') as f:
            img = requests.get(item['url'])
            f.write(img.content)


def main(keyword, page):
    text = get_page(keyword, page)
    items = parse_page(text)
    save_pics(items, page)


if __name__ == '__main__':
    for page in range(30, 121, 30):
        main('热裤', page)