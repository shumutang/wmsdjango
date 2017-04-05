# -*-coding:utf-8-*-

from __future__ import unicode_literals

from django.db import models

from order.models import OrderInProductship, OrderOutProductship
from wms.models import Product

# Create your models here.

class Store(models.Model):
    product_id = models.ForeignKey(Product, verbose_name=u'商品编码')
    check_store = models.IntegerField(u'盘点库存',null=True,blank=True)

    class Meta:
        verbose_name = u'库存报表'
        verbose_name_plural = u'库存报表'
