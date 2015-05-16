#!/usr/bin/env python
#coding=utf-8
import urllib
import re 
import os

#因为妹子图网站中，最底层分类，网页格式都是http://www.meizitu.com/a/5000.html格式，只是数字不同
#所以可以通过循环获取所有url，知道返回的页面中包含title='对不起，出错啦 | 妹子图'为止
#循环中需要获取每页中的去掉后面' | 妹子图'的title和class="postContent"中的所有jpg格式的图片url
#如http://pic.meizitu.com/wp-content/uploads/2012a/03/29/01.jpg

#用来获取网页内容
def getHtml(url):
    file = urllib.urlopen(url)
    html = file.read()
    return html

#用来获取title，并返回一个列表
def gettitle(html):
    reg = r'<title>.*</title>'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    return imglist

#用来获取图片url，并返回一个列表
def getImg(html):
    reg = r'http://pic.meizitu.com/wp-content/uploads/...../../../...jpg'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    return imglist

#下载
def download(imgList,title):
    basic=r'E:/meizitu/'
    dir=basic+title+'/'
    if not os.path.isdir(dir):
		os.makedirs(dir)
		a=1
		for imgurl in imgList:
			#print 'download file start'
			urllib.urlretrieve(imgurl, dir+'%s.jpg' %a)
			#print 'download file '+str(a)+' end'
			a+=1

#测试获取图片url
def test():
	for i in range(94,5000):
		htmlurl=r'http://www.meizitu.com/a/'+str(i)+'.html'
		htmltext=getHtml(htmlurl)
		title=gettitle(htmltext)[0]
		atitle=title[title.find('>')+1:title.find(' ')]
		print atitle
		piclist=getImg(htmltext)
		download(piclist,atitle)
	
if __name__=='__main__':
	test()

