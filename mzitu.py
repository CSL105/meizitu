# coding:utf-8

import requests
from bs4 import BeautifulSoup
import bs4
import os

base_dir = r'E:\workspace\mzitu'

if os.path.exists(base_dir):
    pass
else:
    os.mkdir(base_dir)

headers = {'User-Agent': '''Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)
                            Chrome/47.0.2526.106 Safari/537.36'''}
session = requests.session()
session.headers.update(headers)

menuurls = []

for i in range(20, 30):
    pageurl = 'http://www.mzitu.com/page/%s/' % i
    r = session.get(pageurl)
    soup = BeautifulSoup(r.content, "html.parser")
    for s in soup.find('ul', id='pins').find_all('a'):
        if type(s) == bs4.element.Tag:
            menuurls.append(s.attrs['href'])

menuurls = {}.fromkeys(menuurls).keys()
print(len(menuurls))

for mpicurl in menuurls:
    r = session.get(mpicurl)
    soup = BeautifulSoup(r.content, "html.parser")
    maxnum = int(soup.find('div', class_='pagenavi').find_all('a')[-2].string)
    picimg = soup.find('div', class_="main-image").find('img')
    name = picimg['alt']
    picurl = picimg['src']

    picdir = os.path.join(base_dir, name)
    picdir = picdir.replace('?', '_')

    if os.path.exists(picdir):
        continue
    else:
        os.mkdir(picdir)
        print name, picurl
        print('下载中。。。')

    basepicurl = picurl[0:picurl.rfind('.')-2]+'%s'+picurl[picurl.rfind('.'):]

    for picnum in range(1, maxnum+1):
        picnumstr = str(picnum)
        if len(picnumstr) == 1:
            picnumstr = '0'+picnumstr
        picurl = basepicurl % picnumstr
        pic = session.get(picurl, stream=True).content
        picname = picnumstr + picurl[picurl.rfind('.'):]
        try:
            with open(os.path.join(picdir, picname), "wb") as jpg:
                jpg.write(pic)
        except IOError:
            print("IO Error\n")
        finally:
            jpg.close
    print('下载完成，共 %s 张' % maxnum)

