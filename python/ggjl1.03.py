#coding=utf-8


from queue import Queue

import requests
import simplejson as json

import gevent
from gevent import monkey
monkey.patch_all(thread=False, socket=False)
from bs4 import BeautifulSoup

q = Queue()
url = []

def url_list(code):

    url = 'http://stockpage.10jqka.com.cn/%s/company/' % code #URL构造
    print (url)
    return url


def text_create(item,table_info):
    print ("all length")
    print (len(table_info))
    item = str(item)
    code_path = 'D:/st//'
    full_path = code_path +item + '.txt'    #也可以创建一个.doc的word文档
    with open(full_path, "w", encoding='utf-8') as f:
        for item in table_info:
            f.write("{}\n".format(item))

def req(url):

    headers = {
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.1244 Safari/537.36',
           'Referer': 'http://stock.10jqka.com.cn/',
           'Cookies': 'historystock=000970; Hm_lvt_78c58f01938e4d85eaf619eae719i83e=1505291405,1505302056,1505352637; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1505352637'
    }
    resp = requests.get(url, headers=headers, timeout=3)
    return resp.content  #获取网页内容


def parse_table(soup, code):

        persons = []
        directors = []  # 所有成员
        try:
            tab = soup.findAll("div", {"id": "ml_001"})[0]
        except IndexError:
            tab = soup.findAll("div")
        #print (tab)
        for person in tab.findAll('a', {"class": "turnto"}):
            persons.append(person.text)
        for intro in tab.findAll('td', {"class": "mainintro"}):
            for p in intro.findAll('p')[0]:
                directors.append(p)

        print (persons)
        print (len(directors))
        return directors


def get_soup(resp):
    soup = BeautifulSoup(resp, 'lxml')
    return soup

def load_exist():
    try:
        with open("url.json", "r") as f:
            data = json.load(f)
            url = data["data"]
            return url
    except:
        url = []
        return url

def exist_write(url):
    with open("url.json", "w") as f:
        d = {"data": url}
        json.dump(d, f)

def consumer():
    while not q.empty():
        item = q.get()
        item = item.strip()
        url = url_list(item)
        resp = req(url)
        soup = get_soup(resp)
        try:
            table_info = parse_table(soup, item)
        except:
            pass
        text_create(item,table_info)


def producer():
    headers = {
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.1244 Safari/537.36',
           'Referer': 'http://www.ctxalgo.com/' 
    }
    code_api = requests.get("http://www.ctxalgo.com/api/stocks", headers=headers)
    code_dict = code_api.json()
    code = code_dict.keys() # all lists
    stock_list = [item[-6:] for item in code]
    #code = ['838944']

    for i in stock_list:
        q.put(i)
    print("producer done")

def pre_worker():
    gevent.spawn(consumer).join()
    gevent.spawn(consumer).join()
    print("pre_worker")


def main():
    producer()
    pre_worker()


if __name__ == '__main__':
    main()
