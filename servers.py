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
        if re.fullmatch('(?=.*?[0-9])(?=.*?[A-Za-z]).+', name):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_entries(self, n_letters: int = 3):
        # raise NotImplementedError
        products_list = self.get_all_products(n_letters)
        regex = r'^[a-zA-Z]{' + str(n_letters) + r'}\d{2,3}$'
        # super(get_all_products())
        entries = []
        for p in products_list:
            if re.match(regex, p.name):
                entries.append(p)
            if len(entries) > self.n_max_returned_entries:
                raise TooManyProductsFoundError(val=len(entries), new_value=self.n_max_returned_entries)
        # return entries #tuaj są nieposortowana lista
        return sorted(entries, key=lambda price_of_product: price_of_product.price)


# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania

class ListServer(Server):
    def __init__(self, products: List[Product], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.products = products

    def get_all_products(self, n_letters: int = 3):
        answer = []
        for i in self.products:
            valid_item = re.search(r'^[a-zA-Z]{' + str(n_letters) + r'}\d{2,3}$', i.name)
            print(i.name)
            print(re.fullmatch(r'^[a-zA-Z]{' + str(n_letters) + r'}\d{2,3}$', i.name))

            if valid_item:
                answer.append(i)
            if len(answer) > self.n_max_returned_entries:
                raise TooManyProductsFoundError(val=len(answer), new_value=self.n_max_returned_entries)
        return answer


class MapServer(Server):
    # TODO: type hinting dla dicta
    def __init__(self, products: List[Product], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.products: Dict[str, Product] = {product.name: product for product in products}

    def get_all_products(self, n_letters: int = 1) -> List[Product]:
        answer = []
        for prod_name in self.products:
            valid_item = re.search(r'^[a-zA-Z]{' + str(n_letters) + r'}\d{2,3}$', prod_name)
            if valid_item:
                answer.append(self.products[prod_name])
            if len(answer) > self.n_max_returned_entries:
                pass
        return answer


HelperType = TypeVar('HelperType', bound=Server)


class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer
    # FIXME albo łączną cenę produktów,
    # FIXME albo None – w przypadku, gdy serwer rzucił wyjątek lub gdy nie znaleziono ani jednego produktu spełniającego kryterium

    def __init__(self, server: HelperType):
        self.Server: server = server
        self.Server: server.n_max_returned_entries

    def get_total_price(self, n_letters: int) -> Optional[float]:
        try:
            entries = self.Server.get_entries(n_letters)
        except TooManyProductsFoundError:
            return None
        if len(entries) == 0:
            return None
        total_amount = 0
        for elem in entries:
            total_amount += elem.price
        return total_amount
