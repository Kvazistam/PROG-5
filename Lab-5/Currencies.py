
import time

import requests


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Currencies(metaclass=Singleton):

    def __init__(self):
        self._url = u"https://www.cbr.ru/scripts/XML_daily.asp"
        self.__cur_lst = self.parse_xml(self._url)
        self._time_rate = 1
        self.__cur_time = time.time()

    def parse_xml(self,url) -> dict:
        from xml.etree import ElementTree
        data = requests.get(self._url)
        tree = ElementTree.fromstring(data.content)
        for elem in tree:
            print(*elem)

    def visualize_currencies(self):
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        currencies = []
        for el in self.__cur_lst:
            currencies.append(str(el.keys()))

        print(currencies)

Currencies()