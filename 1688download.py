#!/usr/bin/env python
#coding=utf-8
import urllib
import re 
import os
import sqlite3
import gc
import sys
from PyQt4 import QtGui, QtCore


#获取图片链接，需要参数包含图片连接的网页内容
def getImg(html,reg):
    #reg = r'http://.*?.jpg'  #懒惰匹配，最小匹配，*后面加个？号就行，默认是贪婪匹配
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    return imglist

#图片下载，需要参数图片地址和保存地址
def down_img(imgurl,dir):
	urllib.urlretrieve(imgurl,dir)


#用来获取网页内容
def getHtml(url):
    file = urllib.urlopen(url)
    html = file.read()
    return html
	
def download_imgs(url_product):
    print url_product
    html_product=getHtml(url_product)
    urls_img=re.compile(r'data-tfs-url="(.*?)"',re.DOTALL).search(html_product).group(1)
    html_img=getHtml(urls_img)
    imgs=getImg(html_img,r'http://.*?.jpg')
    productid=re.compile(r'offer/(\d*?).h',re.DOTALL).search(url_product).group(1)
    masterdir=r'E:/download/'
    productdir=masterdir+str(productid)+'/'
    if not os.path.isdir(productdir):
        os.makedirs(productdir)
        title=re.compile(r'<title>(.*?)</title>',re.DOTALL).search(html_product).group(1)
        #title=title.encode('utf-8')
        #cu.execute("delete from product where productid="+productid)
        #cu.execute("insert into product(productid,productname,producturl) values ("+productid+",\'"+title+"\',\'"+url_product+"\')")
        #cx.commit()
        imgname=1
        print 'begin download:'+title+'......'
        for img in imgs:
            down_img(img,productdir+'%s.jpg' %imgname)
            #cu.execute("delete from product_img_url where productid=\'"+productid+"\' and imgid=\'"+str(imgname)+"\'")
            #cu.execute("insert into product_img_url (productid,imgid,productname,imgurl) values ("+productid+","+str(imgname)+",\'"+title+"\',\'"+img+"\')")
            imgname=imgname+1
        #cx.commit()
        f=open(productdir+'1.txt','w')
        f.write(url_product)
        f.close()
        print 'download:'+title+' success'

class Window( QtGui.QWidget ):
    def __init__( self ):
        super( Window, self ).__init__()
        self.setWindowTitle( "Down Load Img From 1688" )
        self.resize( 300, 300 )
         
        gridlayout = QtGui.QGridLayout()
         
        self.AboutButton = QtGui.QPushButton( "All" )
        gridlayout.addWidget( self.AboutButton, 1, 0,1,1 )
        
        self.AboutButton2 = QtGui.QPushButton( "One" )
        gridlayout.addWidget( self.AboutButton2, 1, 1,1,1 )
        
        self.textArea = QtGui.QTextEdit()
        self.textArea.setText( "" )
        gridlayout.addWidget( self.textArea,0,0,1,2 )
        
        spacer = QtGui.QSpacerItem( 50, 50 )
        gridlayout.addItem( spacer, 1, 1, 1, 1 )
        self.setLayout( gridlayout )
         
        self.connect( self.AboutButton, QtCore.SIGNAL( 'clicked()' ), self.OnAboutButton )
        self.connect( self.AboutButton2, QtCore.SIGNAL( 'clicked()' ), self.OnAboutButton2 )
    
    def OnAboutButton( self ):
        company_url=str(self.textArea.toPlainText())
        
        company_html=company_url
        all_product_first_url=re.compile(r'(http://..+?.1688.com)',re.DOTALL).search(company_html).group(1)+'/page/offerlist.htm'
        print all_product_first_url
        all_product_first_html=getHtml(all_product_first_url)
        #http://detail.1688.com/offer/1234563140.html
        #第一页上的所有产品
        all_product_urls=getImg(all_product_first_html,r'http://detail.1688.com/offer/\d*?.html')
        
        all_product_alter_urls=getImg(all_product_first_html,r'<a  href="('+all_product_first_url+r'.*?)">\d')
        
        for all_product_alter_url in all_product_alter_urls:
            all_product_alter_html=getHtml(all_product_alter_url)
            all_product_urls=all_product_urls+getImg(all_product_alter_html,r'http://detail.1688.com/offer/\d*?.html')
        
        all_product_urls=list(set(all_product_urls))
        for all_product_url in all_product_urls:
            download_imgs(all_product_url)
            gc.collect()
        QtGui.QMessageBox.about( self, 'PyQt', "success" )
    
    def OnAboutButton2( self ):
        url=self.textArea.toPlainText()
        #QtGui.QMessageBox.about( self, 'PyQt', str(url) )
        download_imgs(str(url))
        QtGui.QMessageBox.about( self, 'PyQt', 'success' )
    
app = QtGui.QApplication( sys.argv )
win = Window()
win.show()
app.exec_()
