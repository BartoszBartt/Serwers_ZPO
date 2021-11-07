#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Optional, List, Union, TypeVar, Sized, Dict
from abc import ABC, abstractmethod
import re


class Product:
    # TODO: zweryfikowac warunek na nazwe(1 litera/ 1 cyfra) // warunek na unikalna reprezentacje tego samego produktu
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str) i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu float)
    products = None

    def __init__(self, name: str, price: float):
        if re.fullmatch('[a-zA-Z]+[0-9]+', name):
            self.name = name
            self.price = price
            # self.name_char = [i for i in name]
        else:
            raise ValueError

    def __eq__(self, other):
        return self.price == other.price and self.name == other.name  # FIXME: zwróć odpowiednią wartość

    def __hash__(self):
        return hash((self.name, self.price))


class TooManyProductsFoundError:
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    pass


class Server(ABC):
    
    @abstractmethod
    def get_all_products(self):
        raise NotImplementedError

    def get_entries(self):
        pass


# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania

class ListServer(Server):
    n_max_returned_entries: int

    def __init__(self, list_of_products: List[Product]):
        self.list_of_products = list_of_products
        # NIEPEWNE: nw czy to ma byc Product.products czy moze self.products  czy cos innego ~Luki
        Product.products = list

    def get_all_products(self, n_letters: int = 1):
        answer = []
        for i in self.list_of_products:
            valid_item = re.search(r'^[a-zA-Z]{' + str(n_letters) + r'}\d{2,3}$', i.name)
            if valid_item:
                answer.append(i)
            if len(answer) > self.n_max_returned_entries:
                pass


class MapServer(Server):
    n_max_returned_entries: int

    # TODO: type hinting dla dicta
    def __init__(self, dict_of_products: Dict[str, float]):
        self.dict_of_products = dict_of_products
        # NIEPEWNE: nw czy to ma byc Product.products czy moze self.products  czy cos innego ~Luki
        Product.products = dict

    def get_all_products(self, n_letters: int = 1):
        answer = []
        for k, v in self.dict_of_products.items():
            valid_item = re.search(r'^[a-zA-Z]{' + str(n_letters) + r'}\d{2,3}$', k)
            if valid_item:
                answer.append(Product(k, v))
            if len(answer) > self.n_max_returned_entries:
                pass


HelperType = TypeVar('HelperType', bound=Server)


class Client:

    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer

    def __init__(self, Server: HelperType):
        self.server = Server

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        raise NotImplementedError()

class ServerError(Exception):
    pass

class TooManyProductsFoundError(ServerError):
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    def __init__(self, val: float, new_value: float):
        self.val = val
        self.new_value = new_value
        self.message = f'There is too many products: {self.val},there should be {self.new_value} products'

    def __str__(self):
        return self.message

# product_1 = Product("KoX", 2.5)

# print(product_1.name[0], product_1.price)
# print(product_1.name_char)
