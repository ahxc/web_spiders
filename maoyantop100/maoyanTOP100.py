import requests
import re
import time
import json

def get_one_page(url):
    # 新增403报错
    # header更新可在浏览器输入about:version获取
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
        }
    response = requests.get(url, headers)

    if response.status_code == 200:
        response.encoding = 'utf-8' # 新增html为乱码

        return response.text

    return None

def parse_one_page(html, pattern):
    # 编译对象，提高匹配速率
    pattern = re.compile(pattern, re.S)

    items = re.findall(pattern, html)
    # print(html)
    # print(items)

    for item in items:
        yield {
            'top': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4][5:],
            'score': item[5].strip() + item[6].strip()
        }
    # print(items)

    return items

def write_to_file(content):
    # 所有信息
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False)+'\n')
    
    # 封面
    with open('top-'+content['top']+'.jpg', 'ab') as f:
        img = requests.get(content['image'])
        f.write(img.content)

def main(offset, pattern):
    url = 'https://maoyan.com/board/4?offset='+str(offset)
    html = get_one_page(url)
    print(html)

    for item in parse_one_page(html, pattern):
        write_to_file(item)

# 排名，封面，电影名，主演，上映时间，评分整数、小数
# ()标记一个字符串
patterns = '<dd>'\
          +'.*?board-index.*?>(.*?)</i>'\
          +'.*?data-src="(.*?)@.*?"'\
          +'.*?title="(.*?)"'\
          +'.*?star.*?>(.*?)</p>'\
          +'.*?releasetime.*?>(.*?)</p>'\
          +'.*?integer.*?>(.*?)</i>'\
          +'.*?fraction.*?>(.*?)</i>'\
          +'.*?</dd>'

if __name__ == '__main__':
    for i in range(1):
        main(i*10, patterns)
        time.sleep(10)