#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from abc import ABC, abstractmethod
from typing import Optional, List, TypeVar, Dict


class Product:
    # TODO: zweryfikowac warunek na nazwe(1 litera/ 1 cyfra) // warunek na unikalna reprezentacje tego samego produktu
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str) i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu float)
    products = None

    def __init__(self, name: str, price: float):
        if re.fullmatch('[a-zA-Z] + [0-9]+', name):
            self.name = name
            self.price = price
        else:
            raise ValueError

    def __eq__(self, other):
        return self.price == other.price and self.name == other.name  # FIXME: zwróć odpowiednią wartość

    def __hash__(self):
        return hash((self.name, self.price))


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


class Server(ABC):
    n_max_returned_entries = 3

    @abstractmethod
    def get_all_products(self, n_letters: int = 1):
        raise NotImplementedError

    def get_entries(self, n_letters: int = 1):
        ls: List[Product] = self.get_all_products(n_letters=n_letters)

        if not ls:
            return []
        if len(ls) > self.n_max_returned_entries:
            raise TooManyProductsFoundError(val=len(ls), new_value=self.n_max_returned_entries)
        return sorted(ls, key=lambda prod_price: prod_price.price)

# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania

class ListServer(Server):

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
        return answer


class MapServer(Server):

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
        return answer


HelperType = TypeVar('HelperType', bound = Server)


class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer
    # FIXME albo łączną cenę produktów,
    # FIXME albo None – w przypadku, gdy serwer rzucił wyjątek lub gdy nie znaleziono ani jednego produktu spełniającego kryterium

    def __init__(self, server: Server, *args, **kwargs):
        self.server = server

    def get_total_price(self, n_letters: int) -> Optional[float]:
        total_amount = 0
        if len(self.server.get_entries()) == 0 or  :
            return None
        else:
            for i in self.server.get_entries( ):
                total_amount += i.price
        return total_amount
        # raise NotImplementedError()