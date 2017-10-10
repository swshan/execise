import queue
import threading

q = queue.Queue()

class Consumer(threading.Thread):
    def __init__(self, item):
        threading.Thread.__init__(self)
        self.item = item
        self.start()

    def run(self):
        print ("hello thread, %s" % self.item)


def main():

    thread = []
    for i in range(4):
        i = Consumer(i)
        thread.append(i)
    for x in thread:
        x.join()


main()
