from gevent.queue import Queue
import gevent
from gevent import monkey

import requests
monkey.patch_all()

urls = ['https://www.douban.com/group/topic/107676096/',
        'https://www.douban.com/group/topic/107676096/', 
        'https://www.douban.com/group/topic/107635711/',
        'https://www.douban.com/group/topic/107676096/',
        'https://www.douban.com/group/topic/107676096/',
        'https://www.douban.com/group/topic/107676096/',
        'https://www.douban.com/group/topic/106606380/']
	
q = Queue()

def producer(urls):
    for i in urls:
        q.put(i)

def worker():

    while not q.empty():
        url = q.get_nowait() # better to use get_nowait() method, or it will cause bub loopexit.
        print (url)
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=3)


if __name__ == '__main__':
    
    gevent.spawn(producer, urls).join()

    gevent.joinall([
    gevent.spawn(worker,),
    gevent.spawn(worker,)
    ])
    '''
    producer(urls)
    worker()
    ''' 