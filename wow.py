# -*- coding: utf-8 -*-
import codecs
import csv
import time
import requests
from bs4 import BeautifulSoup
import MySQLdb
import shutil, errno
import os
def getHTML(url):
    r = requests.get(url)
    return r.content


def parseHTML(html):
    soup = BeautifulSoup(html,'html.parser')
    target1 = soup.findAll('tr',attrs={'class':'rowtemplate1'})
    target2 = soup.findAll('tr',attrs={'class':'rowtemplate2'})
    info = []
    for template1 in target1:
        mid = template1.find('td',attrs={'class':'tblcellid'}).find('a').get_text()
        yr = template1.find('td',attrs={'class':'tblcellyear'}).get_text()
        make = template1.find('td',attrs={'class':'tblcellmake'}).get_text()
        model = template1.find('td',attrs={'class':'tblcellmodel'}).get_text()
        cc = template1.find('td',attrs={'class':'tblcellcc'}).get_text()
        miles = template1.find('td',attrs={'class':'tblcellmiles'}).get_text()
        price = template1.find('td',attrs={'class':'tblcellprice'}).get_text()
        info.append([mid.encode('utf-8'),yr.encode('utf-8'),make.encode('utf-8'),model.encode('utf-8'),cc.encode('utf-8'),miles.encode('utf-8'),price.encode('utf-8')])
        
    for template1 in target2:
        mid = template1.find('td',attrs={'class':'tblcellid'}).find('a').get_text()
        yr = template1.find('td',attrs={'class':'tblcellyear'}).get_text()
        make = template1.find('td',attrs={'class':'tblcellmake'}).get_text()
        model = template1.find('td',attrs={'class':'tblcellmodel'}).get_text()
        cc = template1.find('td',attrs={'class':'tblcellcc'}).get_text()
        miles = template1.find('td',attrs={'class':'tblcellmiles'}).get_text()
        price = template1.find('td',attrs={'class':'tblcellprice'}).get_text()
        info.append([mid.encode('utf-8'),yr.encode('utf-8'),make.encode('utf-8'),model.encode('utf-8'),cc.encode('utf-8'),miles.encode('utf-8'),price.encode('utf-8')])

    return info
'''
    #print(soup)
    body = soup.body
    fm1 = body.find('form',attrs={'id':'aspnetForm'})
    wrap = fm1.find('div',attrs={'class':'wrap'})
    roadbgdiv = wrap.find('div',attrs={'class':'road_bg_div'})
    gradualdiv = roadbgdiv.find('div',attrs={'class':'gradual_div'})
    ctc = gradualdiv.find('div',attrs={'class':'content_circle'})
    cm = ctc.find('div',attrs={'class':'circle_mid'})
    dpd = cm.find('div',attrs={'class':'detail_page_div'})
    t1 = dpd.find('table',attrs={'class':'searchresults'})
    #tbody = t1.find('tbody')
    #print(tbody)
    
    tr1 = t1.find('tr')
    td1 = tr1.find('td')
    div1 = td1.find('div')
    #longdiv = div1.find('div',attrs={'id':'divTableWithFloatingHeader'})
    #print(div1)
    longta = div1.find('table',attrs={'class':'tableWithFloatingHeader'})
    #tb2 = longta.find('tbody')
    tb2 = longta.find('tr')
'''
    
    
    



URL = 'http://www.wowmotorcycles.com/Bikesearch.aspx'
html = getHTML(URL)
data_list = parseHTML(html) 
print(len(data_list))
#for i in range(len(data_list)):
   # print(data_list[i][0])
csvfile = file('/tmp/WOWmotorcycleQuote.csv','wb')
writer = csv.writer(csvfile)
writer.writerow(['ID','Year','Make','Model','CC','Miles','Price'])
writer.writerows(data_list)
csvfile.close()
data = csv.reader(open('/tmp/WOWmotorcycleQuote.csv'),delimiter=',')  
data.next()
sortedlist = sorted(data, key = lambda x: (x[0], (x[4])))
csvfile2 = file('WOWmotorcycleQuoteSorted.csv','wb')
with open("WOWmotorcycleQuoteSorted.csv", "wb") as f:  
    fileWriter = csv.writer(f, delimiter=',')  
    fileWriter.writerow(['ID','Year','Make','Model','CC','Miles','Price'])
    for row in sortedlist:  
        fileWriter.writerow(row)  
f.close()  

'''
Insert Data to MySQL DataBase
'''
db = MySQLdb.connect(host='localhost',user='root',passwd='mysql',db='java1',port=3306)
cursor = db.cursor()  
sql1 = "load data local infile \'/tmp/WOWmotorcycleQuote.csv\' into table java1.WOWQUOTE fields terminated by ',' optionally enclosed by '\"' escaped by '\"' lines terminated by '\n';"
sql2 = "delete from java1.WOWQUOTE where ID = \'ID\';"
sql3 = "create table java1.temp as select distinct * from java1.WOWQUOTE;"
sql4 = "Drop table java1.WOWQUOTE;"
sql5 = "rename table java1.temp to java1.WOWQUOTE;"
sql6 = "SELECT * from java1.WOWQUOTE order by ID INTO OUTFILE \'/tmp/PriceInspection.csv\' fields terminated by \',\' optionally enclosed by \'\' lines terminated by '\n';"
#
try:
    cursor.execute(sql1)
    cursor.execute(sql2)
    cursor.execute(sql3)
    cursor.execute(sql4)
    cursor.execute(sql5)
    cursor.execute(sql6)
    db.commit()
except:
    db.rollback()

cursor.close()
db.close()

#Duplication


def deleteFile(file):
    if os.path.exists(file):
        os.remove(file)
        print 'Delete temp PriceInspection File successfully!'
    else:
        print 'no such file:%s' % file

#path = "/Desktop/"
#source = os.listdir(path)
#destination = "~/Users/Yuzhou/Desktop/MyWEB"
def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
            print 'Copy file successfully!'
        else: raise
copyanything("/tmp/PriceInspection.csv","/Users/Yuzhou/Desktop/PriceInspection.csv")
deleteFile('/tmp/PriceInspection.csv')