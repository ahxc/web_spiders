from urllib.parse import urlencode, quote, unquote
import requests, urllib, json, os, sys


def get_page(keyword, page):
    keyword = quote(keyword)
    headers = {
        'Host': 'image.baidu.com',
        'Referer': 'http://image.baidu.com/search/index?tn=baiduimage&fm=result&ie=utf-8&word={}'.format(keyword),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
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
    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        print(e)
        return None


def parse_page(json):
    if json.get('data'):
        for item in json.get('data'):
            if item.get('middleURL'):
                image_url = item.get('middleURL')
                yield{
                    'url': image_url
                }


def save_pics(pic_dir_name, url_path, items, page):
    for i, item in enumerate(items):
        with open(url_path, 'a', encoding='utf-8') as f:
            f.write(item['url']+'\n')
        pic_path = os.path.join(pic_dir_name, str(page)+'-'+str(i)+'.jpg')
        with open(pic_path, 'ab') as f:
            img = requests.get(item['url'])
            f.write(img.content)


def main(keyword, page, pic_dir_name, url_path):
    text = get_page(keyword, page)
    items = parse_page(text)
    save_pics(pic_dir_name, url_path, items, page)


if __name__ == '__main__':
    keyword = sys.argv[1]
    number = int(sys.argv[2]) + 1
    try:
        object_name = sys.argv[3]
    except:
        object_name = keyword
    pic_dir_name = object_name
    url_path = object_name+'.txt'
    os.makedirs(pic_dir_name)
    for page in range(30, number, 30):
        main(keyword, page, pic_dir_name, url_path)