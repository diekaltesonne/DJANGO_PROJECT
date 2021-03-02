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


