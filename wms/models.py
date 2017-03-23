# -*-coding:utf-8-*-

from __future__ import unicode_literals

from django.utils import timezone

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


# Create your models here.

@python_2_unicode_compatible
class Customer(models.Model):
    customer_id = models.IntegerField('客户编码',help_text=u'留空系统自动生成',blank=True)
    name = models.CharField('客户名称', max_length=60)
    address = models.CharField('地址', max_length=80)
    city = models.CharField('城市', max_length=20)
    tel = models.CharField('电话', max_length=15)
    phone = models.CharField('手机', max_length=11)
    email = models.EmailField('邮箱', max_length=75, blank=True)

    class Meta:
        verbose_name = u'客户'
        verbose_name_plural = u'客户'

    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        if self.customer_id is None:
            self.customer_id = -1
            super (Customer, self).save (*args, **kwargs)
            self.customer_id = 100000 + self.id
            super (Customer, self).save (*args, **kwargs)


@python_2_unicode_compatible
class Product(models.Model):
    categories_choices = (
        (u'1', u'有条码'),
        (u'2', u'无条码'),
        (u'3', u'其他'),
    )
    base_unit_choices = (
        (u'1', u'箱'),
        (u'2', u'桶'),
        (u'3', u'包'),
        (u'4', u'台'),
        (u'5', u'瓶'),
        (u'6', u'件'),
        (u'9', u'其他'),
    )
    valid_flag_choices = (
        (u'Y', u'Y'),
        (u'N', u'N'),
      )
    product_id = models.IntegerField('商品编码',help_text=u'留空系统会自动生成', blank=True)
    customer = models.ForeignKey(Customer, verbose_name='所属客户')
    name = models.CharField('中文名称', max_length=80)
    ename = models.CharField('英文名称', max_length=30, blank=True, null=True)
    help_name = models.CharField('助记码', max_length=75, blank=True)
    batch_num = models.IntegerField('货物批号', default=100)
    type = models.CharField('型号', max_length=20, blank=True, null=True)
    categories = models.CharField('商品分类', max_length=20,choices=categories_choices,default='1')
    base_unit = models.CharField('基本单位', max_length=6,choices=base_unit_choices,default='1')
    pcs_perunit = models.IntegerField('PCS/箱', default=1)
    Logistics_unit = models.CharField('物流单位', max_length=10, choices=base_unit_choices,blank=True, null=True)
    pcs_Logistics = models.IntegerField('PCS/标准板', default=1)
    life_day = models.IntegerField('保质期(天)', default=0)
    price = models.DecimalField('单价', max_digits=10, decimal_places=2, null=True, blank=True)
    width = models.IntegerField('宽度(CM)', default=0)
    height = models.IntegerField('高度(CM)', default=0)
    length = models.IntegerField('长度(CM)', default=0)
    weight = models.IntegerField('重量(KG)', default=0)
    net_weight = models.IntegerField('净重(KG)', default=0)
    valid_flag = models.CharField('有效标志', max_length=6, default='Y')
    barcode = models.CharField('条形码', max_length=20)
    specs = models.CharField('规格', max_length=60, blank=True, null=True)
    brand = models.CharField('品牌', max_length=20, blank=True, null=True)
    ordinal = models.IntegerField('序号', blank=True, null=True, default=0)

    class Meta:
        verbose_name = u'商品'
        verbose_name_plural = u'商品'

    def __str__(self):
        return self.name

    def volume(self):
        return self.width * self.height * self.length
    volume.short_description = u'体积'

    def save(self, *args, **kwargs):
        if self.product_id is None:
            self.product_id = -1
            super(Product, self).save(*args, **kwargs)
            self.product_id = 10000000 + self.id
            super(Product, self).save(*args, **kwargs)


@python_2_unicode_compatible
class Warehouse(models.Model):
    type_choices = (
        (u'normal', u'全品类仓库'),
        (u'blp', u'不良品仓库'),
        (u'zp', u'赠品仓库'),
    )
    name = models.CharField('仓库名称', max_length=80)
    ename = models.CharField('仓库简码', max_length=4, blank=True, null=True)
    address = models.CharField('仓库地址', max_length=75, blank=True)
    type = models.CharField('仓库类型', max_length=8, choices=type_choices, default='normal')

    class Meta:
        verbose_name = u'仓库'
        verbose_name_plural = u'仓库'

    def __str__(self):
        return self.ename

class CommonOrder(models.Model):
    order_type_choices = (
        (u'入库', (
            ('a', u'正常入库'),
            ('b', u'不良品入库'),
            ('c', u'赠品入库'),
        )
         ),
        (u'出库', (
            ('d', u'正常出库'),
            ('e', u'赠品出库'),
        )
         ),
        (u'其他', (
            ('f', u'未知'),
        )
         ),
    )

    order_state_choices = (
        (u'1', u'接单'),
        (u'2', u'操作中'),
        (u'3', u'已入库'),
        (u'4', u'已出库'),
    )

    in_store_choices = (
        (u'1', u'是'),
        (u'2', u'否'),
    )
    customer = models.ForeignKey(Customer, verbose_name='所属客户')
    warehouse = models.ForeignKey(Warehouse, verbose_name='操作仓库')
    serial_number = models.CharField('订单流水(系统自动生成)', max_length=16, null=True, blank=True)
    invoice = models.IntegerField('发票号')
    pcs = models.IntegerField('订单pcs')
    boxes = models.IntegerField('合计箱数')
    in_store = models.CharField('入库', max_length=4, choices=in_store_choices,default='2')
    order_type = models.CharField('订单类型', max_length=10, choices=order_type_choices, default='1')
    order_comment = models.CharField('订单备注', max_length=60, null=True, blank=True)
    order_state = models.CharField('订单状态', max_length=10, choices=order_state_choices)
    operate_date = models.DateField('操作日期', null=True, blank=True,default=timezone.now)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class OrderIn(CommonOrder):
    in_number = models.CharField('入库编号', help_text=u'留空系统会自动生成', max_length=20, blank=True)
    sender = models.CharField('结算单位', max_length=30, blank=True, null=True)
    receiver = models.CharField('送货单位', max_length=30, blank=True, null=True)
    plan_in_time = models.DateField('计划入库日期', blank=True, null=True)
    operator = models.CharField('制单人', max_length=60, null=True, blank=True)
    fact_in_time = models.DateField('实际入库日期', null=True, blank=True)
    product = models.ManyToManyField(Product, verbose_name='商品名称', through='OrderInProductship')

    class Meta:
        verbose_name = u'订单(入库)'
        verbose_name_plural = u'订单(入库)'
        ordering = ['plan_in_time']

    def __str__(self):
        return self.in_number

@python_2_unicode_compatible
class OrderOut(CommonOrder):
    out_number = models.CharField('出库编号', help_text=u'留空系统会自动生成', max_length=20)
    fact_out_time = models.DateField('出库日期', null=True, blank=True)
    receiver = models.CharField('收货人', max_length=10, blank=True, null=True)
    receiver_addr = models.CharField('送货地址', max_length=30, blank=True, null=True)
    receiver_phone = models.IntegerField('收货人电话',blank=True, null=True)
    operator = models.CharField('出库人', max_length=60, null=True, blank=True)
    product = models.ManyToManyField(Product, verbose_name='商品名称', through='OrderOutProductship')

    class Meta:
        verbose_name = u'订单(出库)'
        verbose_name_plural = u'订单(出库)'
        ordering = ['fact_out_time']

    def __str__(self):
        return self.out_number


class OrderInProductship(models.Model):
    orderin = models.ForeignKey(OrderIn,verbose_name='订单编号')
    product = models.ForeignKey(Product, verbose_name='商品名称')
    orderin_pcs = models.IntegerField('入库数量', default=0)

    class Meta:
        verbose_name = u'入库订单-商品'
        verbose_name_plural = u'入库订单-商品'


class OrderOutProductship(models.Model):
    orderout = models.ForeignKey(OrderOut)
    product = models.ForeignKey(Product, verbose_name='商品名称')
    orderout_pcs = models.IntegerField('出库数量', default=0)

    class Meta:
        verbose_name = u'出库订单-商品'
        verbose_name_plural = u'出库订单-商品'


class Location(models.Model):
    loca_state_choice = (
        (u'1', u'可用库位'),
        (u'2', u'已用库位'),
    )

    loca_type_choices = (
        (u'1', u'平面仓'),
        (u'2', u'立体仓'),
    )

    loca_category_choices = (
        (u'1', u'全功能'),
        (u'2', u'其他'),
    )

    freeze_flag_choices = (
        (u'Y', u'Y'),
        (u'N', u'N'),
    )

    flag_choices = (
        (u'Y', u'Y'),
        (u'N', u'N'),
    )

    customer = models.ForeignKey(Customer,verbose_name='所属客户')
    warehouse = models.ForeignKey(Warehouse,verbose_name='所属仓库')
    location_id = models.CharField('库位条码', max_length=8)
    state = models.CharField('库位状态', max_length=8,choices=loca_state_choice)
    type = models.CharField('库位类型', max_length=8,choices=loca_type_choices,default=1)
    category = models.CharField('库位类别', max_length=8,choices=loca_category_choices,default=1)
    freeze_flag = models.CharField('冻结标志', max_length=2,choices=freeze_flag_choices,default='N')
    area = models.CharField('仓库区域', max_length=8,null=True,blank=True)
    mixstore = models.CharField('是否混储', max_length=2,choices=flag_choices,default='Y')
    mixbatch = models.CharField('是否混批', max_length=2,choices=flag_choices,default='Y')
    repeate = models.CharField('重复装托', max_length=2,choices=flag_choices,default='Y')
    x = models.IntegerField('X坐标',default=0)
    y = models.IntegerField('Y坐标',default=0)
    z = models.IntegerField('Z坐标',default=0)
    valid_flag = models.CharField('有效标志',max_length=2,choices=flag_choices,default='Y')
    standcode = models.CharField('标准代码', max_length=8)
    up = models.IntegerField('上坐标', default=0)
    left = models.IntegerField('左坐标', default=0)
    length = models.IntegerField('长度', default=0)
    width = models.IntegerField('宽度', default=0)
    volume = models.IntegerField('货物容积', default=0)
    comment = models.CharField('备注', max_length= 80,null=True,blank=True)
    help_tag = models.CharField('助记符',max_length=8,null=True,blank=True)
    name = models.CharField('中文名称', max_length= 16,null=True,blank=True)

    class Meta:
        verbose_name = u'库位'
        verbose_name_plural = u'库位'

    def __str__(self):
        return self.location_id

