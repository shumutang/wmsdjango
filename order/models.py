# -*-coding:utf-8-*-

from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from django.utils import timezone
from datetime import date

from django.core.exceptions import ValidationError

from wms.models import Customer , Product , Location , Warehouse

# Create your models here.

class CommonOrder(models.Model):
    customer = models.ForeignKey(Customer, verbose_name='所属客户')
    warehouse = models.ForeignKey(Warehouse, verbose_name='操作仓库')
    serial_number = models.CharField('订单流水(系统自动生成)', max_length=16, null=True, blank=True)
    invoice = models.IntegerField('发票号', null=True,blank=True)
    pcs = models.IntegerField('订单pcs', null=True, blank=True)
    boxes = models.IntegerField('合计箱数', null=True, blank=True)
    order_comment = models.CharField('订单备注', max_length=60, null=True, blank=True)
    operate_date = models.DateTimeField('操作日期', null=True, blank=True,default=timezone.now)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class OrderIn(CommonOrder):
    order_type_choices = (
            ('zc', u'正常入库'),
            ('bl', u'不良品入库'),
            ('zp', u'赠品入库'),
            ('qt', u'其他'),
    )

    in_store_choices = (
        (u'y', u'已完成'),
        (u'n', u'未完成'),
    )
    in_number = models.CharField('入库编号',primary_key=True, help_text=u'留空系统会自动生成', max_length=20, blank=True)
    sender = models.CharField('结算单位', max_length=30, blank=True, null=True)
    receiver = models.CharField('送货单位', max_length=30, blank=True, null=True)
    plan_in_time = models.DateField('计划入库日期', default=date.today)
    fact_in_time = models.DateField('实际入库日期', default=date.today)
    operator = models.CharField('制单人', max_length=60 , null=True , blank=True)
    in_store = models.CharField('入库', max_length=4, choices=in_store_choices, default='n')
    order_type = models.CharField('订单类型', max_length=10, choices=order_type_choices, default='zc')
    product = models.ManyToManyField(Product, verbose_name='商品名称', through='OrderInProductship')

    class Meta:
        verbose_name = u'订单(入库)'
        verbose_name_plural = u'订单(入库)'
        ordering = ['-in_number']

    def __str__(self):
        return self.in_number

    # def save(self, *args, **kwargs):
    #     if self.in_store == "y":
    #         Msg = u'Order(%s) is completed,do not modified.' % self.in_number
    #         raise ValidationError(Msg)
    #     else:
    #         super(OrderIn, self).save(*args, **kwargs)


@python_2_unicode_compatible
class OrderOut(CommonOrder):
    order_type_choices = (
            ('zc', u'正常出库'),
            ('bl', u'不良品出库'),
            ('zp', u'赠品出库'),
            ('qt', u'其他'),
    )

    out_store_choices = (
        (u'y', u'已完成'),
        (u'n', u'未完成'),
    )

    out_number = models.CharField('出库编号', primary_key=True, help_text=u'留空系统会自动生成', max_length=20, blank=True)
    fact_out_time = models.DateField('出库日期', default=date.today)
    receiver = models.CharField('收货人', max_length=10, blank=True, null=True)
    receiver_addr = models.CharField('送货地址', max_length=30, blank=True, null=True)
    receiver_phone = models.IntegerField('收货人电话',blank=True, null=True)
    operator = models.CharField('出库人', max_length=60, null=True, blank=True)
    out_store = models.CharField('出库', max_length=4, choices=out_store_choices,default='n')
    order_type = models.CharField('订单类型', max_length=10, choices=order_type_choices, default='zc')
    product = models.ManyToManyField(Product, verbose_name='商品名称', through='OrderOutProductship')

    class Meta:
        verbose_name = u'订单(出库)'
        verbose_name_plural = u'订单(出库)'
        ordering = ['-out_number']

    def __str__(self):
        return self.out_number

    # def save(self, *args, **kwargs):
    #     if self.out_store == "y":
    #         Msg = u'Order(%s) is completed,do not modified.' % self.out_number
    #         raise ValidationError(Msg)
    #     else:
    #         super(OrderOut, self).save(*args, **kwargs)


class OrderInProductship(models.Model):
    orderin = models.ForeignKey(
        OrderIn,
        verbose_name='入库编号',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        verbose_name='商品名称',
        on_delete=models.CASCADE,
        parent_link=True
    )
    orderin_pcs = models.IntegerField('入库数量', default=0)

    def save(self, *args, **kwargs):
        if self.orderin.in_store == "y":
            Msg = u'Order(%s) is completed,do not modified.' % self.orderin.in_number
            raise ValidationError(Msg)
        else:
            super(OrderInProductship, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u'入库订单-商品明细'
        verbose_name_plural = u'入库订单-商品明细'
        ordering = ['-id']

class OrderOutProductship(models.Model):
    orderout = models.ForeignKey(
        OrderOut,
        verbose_name='出库编号',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        verbose_name='商品名称',
        on_delete=models.CASCADE
    )
    orderout_pcs = models.IntegerField('出库数量', default=0)

    def save(self, *args, **kwargs):
        if self.orderout.out_store == "y":
            Msg = u'Order(%s) is completed,do not modified.' % self.orderout.out_number
            raise ValidationError(Msg)
        else:
            super(OrderOutProductship, self).save(*args, **kwargs)

    class Meta:
        verbose_name = u'出库订单-商品明细'
        verbose_name_plural = u'出库订单-商品明细'
        ordering = ['-id']

