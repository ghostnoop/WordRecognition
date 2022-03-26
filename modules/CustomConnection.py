import multiprocessing
from multiprocessing.connection import Connection


class CustomConnection:
    def __init__(self, index: int,conn1,conn2):
        # conn1, conn2 = multiprocessing.Pipe(duplex=False)
        self.__receive = conn1
        self.__sendler = conn2
        self.index = index

    def receive(self, wait=True):
        if wait and self.__receive.poll(timeout=60*5):
            obj = self.__receive.recv()
        else:
            obj = self.__receive.recv()
        return obj

    def send(self, obj):
        self.__sendler.send(obj)
