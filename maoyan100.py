import codecs
import requests
from pyquery import PyQuery as pq
from requests.exceptions import RequestException
import csv

def get_one(url):
    try:
        #get请求
        response=requests.get(url)
        #判断是否返回200，如果返回200证明无误，返回url源码
        if response.status_code==200:
            return response.text
        else:
            return None
    except RequestException:
        print("Something Error")

def expl_one(html):
    doc=pq(html)
    l1=doc('.board-wrapper dd').items()
    result=[]
    i=0
    for l2 in l1:
        result2=[]
        result2.append(l2('.board-index').text())
        result2.append(l2('.board-item-main .board-item-content .movie-item-info .name').text())
        result2.append(l2('.star').text().strip()[3:])
        result2.append(l2('.releasetime').text().strip()[5:])
        result2.append(l2('.score').text())
        result2.append(get_intro(l2('.board-item-main .board-item-content .movie-item-info .name a').attr('href')))
        result.append(result2)
        i=i+1
    nextpage=doc(".list-pager li:last-child a").attr('href')
    return result,nextpage

def get_intro(href):
    url='https://maoyan.com'+href
    doc=pq(url)
    return doc('.mod-content .dra').text()

def write2txt(results):
    with open(r"C:\Users\Liter Frye\Desktop\maoyan100.csv", 'a', newline='',encoding='utf-8-sig') as csvfile:
        #csvfile.write(codecs.BOM_UTF8)
        writer = csv.writer(csvfile)
        for row in results:
            writer.writerow(row)

def main():
    url="https://maoyan.com/board/4"
    html=get_one(url)
    result,nextpage=expl_one(html)
    write2txt(result)
    for i in range(9):
        url="https://maoyan.com/board/4"+nextpage
        html = get_one(url)
        result1, nextpage = expl_one(html)
        write2txt(result1)

if __name__ == '__main__':
    main()