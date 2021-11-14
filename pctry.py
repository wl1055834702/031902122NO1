#	coding=gbk
# -*- coding:UTF-8 -*-
#jjjj
import requests
import io
import sys
from bs4 import BeautifulSoup
import urllib.request
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') #改变标准输出的默认编码
if __name__ == '__main__':
    target = 'https://www.biqukan.cc/article/1040/38226640.html'
    req = requests.get(url=target)
    html = req.text
    bf = BeautifulSoup(html,"html.parser")
    texts = bf.find_all('div', class_='showtxt')
    print(texts)
