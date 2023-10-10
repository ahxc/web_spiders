import requests, time, os, re

from hashlib import md5
from lxml import etree
from bs4 import BeautifulSoup
from multiprocessing.pool import Pool
from urllib.parse import urlencode
​
​
def get_page(offset):
    global headers # 全局变量
    headers = {
        'cookie': 's_v_web_id=verify_kew8j0be_8BWl5Sju_4fkF_4TOT_Ahk1_V5BUTkBu2Mde; WEATHER_CITY=%E5%8C%97%E4%BA%AC; MONITOR_WEB_ID=45286aea-8917-401c-8ff5-ba01ed26de84; ttcid=680a144dc3654d978a76776a92bd1bae38; tt_webid=6870770921575122446; tt_webid=6870770921575122446; __tasessionId=5xehoh10s1599726043290; __ac_signature=_02B4Z6wo00f01ufebHQAAIBB.oCKQQk-M.Ln2mjAAOa8q8e9sJt5nRz.Znd9vYPs4qSng4cm9Wno3MlNqIGYlBEDdggqOMkPBzp7WhEY7-5QsG9cfi0-oPytLTmJhGRXtBn8evsLIL3.VbkU1a; tt_scid=7-RlHQ6VYZFM2j4JSEKUN2MtMNZ5n8jWdeOeNbOHJxhb1U9ewZJHqTvmJt2ky.ax7dc4',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
        'referer': 'https://www.toutiao.com/search/?keyword=%E7%BE%8E%E5%A5%B3',
        'x-requested-with': 'XMLHttpRequest'
    }

    params = {
        'aid': '24',
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': '美女',
        'autoload': 'true',
        'count': '20',
        'en_qc': '1',
        'cur_tab': '1',
        'from': 'search_tab',
        'pd': 'synthesis',
        'timestamp': int(time.time()),
        '_signature': 
    }

    url = 'https://www.toutiao.com/api/search/content/?' + urlencode(params)  # 构造url
    url = url.replace('=+', '=')  # 网址根本不一样
    # print(url)
    try:
        r = requests.get(url, headers=headers, params=params)
        r.content.decode('utf-8')
        if r.status_code == 200:
            return r.json()  # 返回json格式 因为全是字典类型
    except requests.ConnectionError as e:
        print(e)
​
​
def get_image(json):
    if json.get('data'):
        for item in json.get('data'):
            if item.get('title') is None:
                continue  # 如果标题是空值
            title = item.get('title')  # 获取标题
            # if item.get('image_list') is None:  # 进行判空
            #     continue
            # urls = item.get('image_list')  # 获得图片网址
            # for url in urls:  # 遍历这个urls
            #     url = url.get('url')
            #     # 使用正则拼接网址
            #     url = 'http://p1.pstatp.com/origin/' + 'pgc-image/' + url.split('/')[-1]
            if item.get('article_url') == None:
                continue
            url_page = item.get('article_url')
            # print(url_page)
            rr = requests.get(url_page, headers=headers)
​
            if rr.status_code == 200:
                pat = '<script>var BASE_DATA = .*?articleInfo:.*?content:(.*?)groupId.*?;</script>'
                match = re.search(pat, rr.text, re.S)
                if match != None:
                    result = re.findall(r'img src&#x3D;\\&quot;(.*?)\\&quot;', match.group(), re.S)
                    # for i in result:
                    #     print(i.encode('utf-8').decode('unicode_escape')
                    # 转换编码方式 把\u之类的改掉
                    yield {
                        'title': title,
                        'image': result
                    }
            #  格式出错，这里产生了十六进制的数值， 网址获取不了，明天看
            # yield {
            #     'title': title,
            #     'image': url
            # }  # 返回标题和网址
​
​
def save_image(content):
    path = 'D://今日头条美女//'  # 目录
    if not os.path.exists(path):  # 创建目录
        os.mkdir(path)
        os.chdir(path)
    else:
        os.chdir(path)
​
    if not os.path.exists(content['title']):  # 创建单个文件夹
        if '\t' in content['title']:  # 以title为标题创建单个文件夹
            title = content['title'].replace('\t', '')  # 去除特殊符号 不然创建不了文件名称
            os.mkdir(title + '//')
            os.chdir(title + '//')
            print(title)
        else:
            title = content['title']
            os.mkdir(title + '//')  # 创建文件夹
            os.chdir(title + '//')
            print(title)
    else:  # 如果存在
        if '\t' in content['title']:  # 以title为标题创建单个文件夹
            title = content['title'].replace('\t', '')  # 去除特殊符号 不然创建不了文件名称
            os.chdir(title + '//')
            print(title)
        else:
            title = content['title']
            os.chdir(title + '//')
            print(title)
    for q, u in enumerate(content['image']):  # 遍历图片地址列表
        u = u.encode('utf-8').decode('unicode_escape')
​
        # 先编码在解码 获得需要的网址链接
        #  开始下载
        r = requests.get(u, headers=headers)
        if r.status_code == 200:
            # file_path = r'{0}/{1}.{2}'.format('美女', q, 'jpg')  # 文件的名字和地址，用三目运算符来调试文件夹的名字
            # hexdisgest() 返回十六进制图片
            with open(str(q) + '.jpg', 'wb') as fw:
                fw.write(r.content)
                print(f'该系列----->下载{q}张')
​
​
def main(offset):
    json = get_page(offset)
    get_image(json)
    for content in get_image(json):
        try:
            # print(content)
            save_image(content)
        except FileExistsError and OSError:
            print('创建文件格式错误，包含特殊字符串:')
            continue
​
​
if __name__ == '__main__':
    pool = Pool()
    groups = [j * 20 for j in range(8)]
    pool.map(main, groups) # 传offset偏移量
    pool.close()
    pool.join()