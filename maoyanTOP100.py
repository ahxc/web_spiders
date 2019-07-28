import requests
import re
import time
import json

def get_one_page(url):
    response = requests.get(url)

    if response.status_code == 200:
        return response.text

    return None

def parse_one_page(html, pattern):
    pattern = re.compile(pattern, re.S)

    items = re.findall(pattern, html)

    for item in items:
        yield {
            'top': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4][5:],
            'score': item[5].strip() + item[6].strip()
        }

    return items

def write_to_file(content):
    # 所有信息
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False)+'\n')
    
    # 封面
    with open('top-'+content['top']+'.jpg', 'ab') as f:
        img = requests.get(content['image'])
        f.write(img.content)

def main(offset):
    url = 'https://maoyan.com/board/4?offset='+str(offset)
    html = get_one_page(url)

    for item in parse_one_page(html, pattern):
        write_to_file(item)

# 排名，封面，电影名，主演，上映时间，评分整数、小数
pattern = '<dd>'\
          +'.*?board-index.*?>(.*?)</i>'\
          +'.*?data-src="(.*?)@.*?"'\
          +'.*?name.*?a.*?>(.*?)</a>'\
          +'.*?star.*?>(.*?)</p>'\
          +'.*?releasetime.*?>(.*?)</p>'\
          +'.*?integer.*?>(.*?)</i>'\
          +'.*?fraction.*?>(.*?)</i>'\
          +'.*?</dd>'

if __name__ == '__main__':
    for i in range(10):
        main(i*10)
        time.sleep(2)
