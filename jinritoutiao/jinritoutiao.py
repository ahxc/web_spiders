from urllib.parse import urlencode

import requests

def get_page(offset, keyword):
    headers = {
        'cookie': 'tt_webid=6667396596445660679; '+\
                  'csrftoken=3a212e0c06e7821650315a4fecf47ac9; '+\
                  'tt_webid=6667396596445660679; '+\
                  'WEATHER_CITY=%E5%8C%97%E4%BA%AC; '+\
                  'UM_distinctid=16b846003e03d7-0dd00a2eb5ea11-353166-1fa400-16b846003e1566; '+\
                  'CNZZDATA1259612802=2077267981-1561291030-https%253A%252F%252Fwww.baidu.com%252F%7C1561361230; '+\
                  '__tasessionId=4vm71cznd1561363013083; '+\
                  'sso_uid_tt=47d6f9788277e4e071f3825a3c36a294; '+\
                  'toutiao_sso_user=e02fd616c83dff880adda691cd201aaa; '+\
                  'login_flag=6859a0b8ffdb01687b00fe96bbeeba6e; '+\
                  'sessionid=21f852358a845d783bdbe1236c9b385b; '+\
                  'uid_tt=d40499ec45187c2d411cb7bf656330730d8c15a783bb6284da0f73104cd300a2; '+\
                  'sid_tt=21f852358a845d783bdbe1236c9b385b; '+\
                  'sid_guard="21f852358a845d783bdbe1236c9b385b|1561363028|15552000|Sat\054 21-Dec-2019 07:57:08 GMT"; '+\
                  's_v_web_id=6f40e192e0bdeb62ff50fca2bcdf2944',

        'user-agent': 'Mozilla/5.0 '+\
                      '(Windows NT 10.0; Win64; x64) '+\
                      'AppleWebKit/537.36 '+\
                      '(KHTML, like Gecko) '+\
                      'Chrome/74.0.3729.157 '+\
                      'Safari/537.36',

        'x-requested-with': 'XMLHttpRequest',

        'referer': 'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D',
    }

    params = {
                'aid': '24',
                'app_name': 'web_search',
                'offset': offset,
                'format': 'json',
                'keyword': keyword,
                'autoload': 'true',
                'count': '20',
                'en_qc': '1',
                'cur_tab': '1',
                'from': 'search_tab',
                'pd': 'synthesis',
        }

    url = 'https://www.toutiao.com/api/search/content/?'+urlencode(params)

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()

    except requests.ConnectionError:
        return None

def parse_page(json):
    if json.get('data'):
        for item in json.get('data'):
            title = item.get('abstract')
            images = item.get('image_list')
        
            if (title is None) or (title == '') or (images is None):
                continue

            pic_list = []
            for image in images:
                pic_list.append(image.get('url'))
                
            yield{
                'title': title,
                'images': pic_list
            }

def save_pics(item):
    for i, url in enumerate(item['images']):
        img = requests.get(url)

        if img.status_code == 200:
            with open(item['title']+'-{}.jpg'.format(i), 'wb') as f:
                f.write(img.content)

        else:
            print(item['title']+' failed to save image')

if __name__ == '__main__':
    
    for offset in range(0, 120, 20):
        json = get_page(offset, '热裤')

        items = parse_page(json)

        for item in items:
            print(item)

            save_pics(item)



