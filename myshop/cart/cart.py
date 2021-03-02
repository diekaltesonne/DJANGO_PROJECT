from decimal import Decimal
from typing import Protocol
from django.conf import settings

from shop.models import Product

class Cart(object):
    def __init__(self,request): 
        ''' иницициализация объекта козрины  '''
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Сохранеяем в сессию пустую корзину.
            cart = self.session[settings.CART_SESSION_ID]
        self.cart = cart

    def add(self, product, quantity = 1, update_quantity = False):
        ''' Добавление товара в корзину или обновление его количества '''
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()
    
    def save(self):
        # Помечаем сессию как измененную
        self.session.modified = True

    def remove(self, product):
        ''' Удаление товара из корзины '''
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        ''' Проходим по товарам корзины и получаем соотвествующие объекты Product. '''
        product_ids = self.cart.keys()
        # Получаем объекты модели Product и передаем их в корзину.
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()

        for product in products:
            cart[str(product_ids)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
        yield item
    
    def __len__(self):
        ''' Возвращает общее количество товаров в корзине '''
        return sum (item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        return sum(
            Decimal(item['price'] * item['quantity'])
            for item in self.cart.values()
        )
    
    def clear(self):
        # Oчистка корзины.
        del self.session[settings.CART_SESSION_ID]
        self.save()


        


