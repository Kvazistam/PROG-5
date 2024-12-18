from __future__ import annotations
from abc import ABC, abstractmethod
import json
from random import randrange
import time
from typing import List

import numpy as np
import requests

from app.app import *


class Subject(ABC):

    @abstractmethod
    def attach(self, observer: Observer) -> None:

        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:

        pass

    @abstractmethod
    def notify(self) -> None:
        pass

class Observer(ABC):


    @abstractmethod
    def update(self, subject: Subject) -> None:
        """
        Получить обновление от субъекта.
        """
        pass


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Currencies(metaclass=Singleton):

    def __init__(self):
        self._url = u"https://www.cbr.ru/scripts/XML_daily.asp"
        self._cur_dict = None
        self._time_pause = 1

    def set_time_pause(self, pause):
        self._time_pause = pause
    
    def get_time_pause(self):
        return self._time_pause 
    
    def set_url(self, url):
        self._url = url
    
    def get_url(self):
        return self._url
    
    def set_cur_dict(self, new_dict):
        self._cur_dict = new_dict
    
    def get_cur_dict(self):
        return self._cur_dict
    
    def get_currencies(self, *names):
        res = self.parse_xml(self._url)
        if res:
            self.set_cur_dict(res)
        if names:
            new_res = [res[name] for name in names]
            return new_res
        # return json.dumps(res)
        return res
        
    def parse_xml(self,url) -> dict:
        from xml.etree import ElementTree
        self.__cur_time = time.time()
        if self.__cur_time - self._time_pause <=0:
            return self.get_cur_dict()
        data = requests.get(self._url)
        tree = ElementTree.fromstring(data.content)
        tree_dict = {str(tree.tag) : tree.attrib}
        for elem in tree:
            p = {val.tag:val.text for val in elem}
            num, ost = map(int, p["Value"].split(','),)
            if int(p["Nominal"]) !=1:
                tree_dict[elem.attrib["ID"]] = {p['CharCode']:(p['Name'],(num, ost), f'номинал: {p['Nominal']}') }
            else:
                tree_dict[elem.attrib["ID"]] = {p['CharCode']:(p['Name'],(num, ost)) }
        return tree_dict
    
    
    def visualize_currencies(self):
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(14, 8))
        currencies = []
        prices = []
        names=[]
        for key in self._cur_dict:
            if key == 'ValCurs':
                continue
            for name in self._cur_dict[key]:
                inform = self._cur_dict[key][name]
                real_name = inform[0]
                nominal = 1
                if len(inform)==3:
                    nominal = int(inform[2].split(' ')[1])
                price = float(f'{inform[1][0]}.{inform[1][1]}')/nominal
                prices.append(price)
                names.append(real_name)
                currencies.append(name)
        colors = plt.cm.viridis(np.linspace(0, 1, len(currencies)))


        plt.xticks(rotation=90, ha="right", fontsize=10)
        ax.bar(currencies, prices, label=names, color=colors)
        ax.set_ylabel('price of currencies in roubles')
        ax.set_xlabel('Currencies')
        ax.set_title('Currencie rate')
        ax.legend(title='currencies rate',loc='center left', bbox_to_anchor=(1, 0.5), fontsize=8)
        plt.subplots_adjust(right=0.8)
        plt.savefig(u'images/Currency_rate.jpg', format='jpg', bbox_inches='tight')


class CurrenciesManager(Subject):
    def __init__(self, time_rate = 600, ):
        super().__init__()
        self.currencies = Currencies()
        self._state: dict = {}
        self.time_rate = time_rate # Время обновления данных с сайта. По дефолту 10 мин.
        self.__cur_time = time.time()
        self._observers = []


    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)


    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)


    async def notify(self) -> None:
        for observer in self._observers:
            await observer.update(self)

    async def update_currencies(self) -> None:
        new_curr = self.currencies.get_currencies()
        if not new_curr:
            print("Тревога")
        self._state = new_curr

        await self.notify()    
        print("yaha")            
        
        
        
class Client(Observer):
    def __init__(self,id: int, websocket: WebSocket,  charcodes=[]):
        super().__init__()
        self.id = id
        self.websocket = websocket
        self.charcodes = charcodes
        self.curr_dict = {}
        
    async def update(self, subject: Subject) -> None:
        if self.charcodes:
            for i in self.charcodes:
                if i == 'ALL':
                    self.charcodes = []
                    self.curr_dict = subject._state
                    return
                else:
                    data = subject._state.get(i)
                    if data is None:
                        continue
                    if data != self.curr_dict.get(i):
                        self.curr_dict[i] = subject._state.get(i)
            await self.websocket.send_json(json.dumps(self.curr_dict, ensure_ascii= False))
        else:
            self.curr_dict = subject._state
            print("ConcreteObserverA: Reacted to the event")
            await self.websocket.send_json(json.dumps(self.curr_dict, ensure_ascii= False))
        

