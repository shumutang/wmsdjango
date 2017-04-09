# -*-coding:utf-8-*-

from __future__ import unicode_literals


from django.db import models
from django.utils.encoding import python_2_unicode_compatible


# Create your models here.

@python_2_unicode_compatible
class Customer(models.Model):
    customer_id = models.IntegerField('客户编码',help_text=u'留空系统自动生成',unique=True, blank=True)
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
        super(Customer , self).save(*args , **kwargs)


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
    barcode = models.BigIntegerField('条形码', primary_key=True,)
    product_id = models.IntegerField('商品编码',help_text=u'留空系统会自动生成', unique=True, blank=True)
    customer = models.ForeignKey(Customer, verbose_name='所属客户')
    name = models.CharField('中文名称', max_length=40)
    ename = models.CharField('英文名称', max_length=20, blank=True, null=True)
    help_name = models.CharField('助记码', max_length=20, blank=True)
    batch_num = models.CharField('货物批号', max_length=20, blank=True)
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
    specs = models.CharField('规格', max_length=60, blank=True, null=True)
    brand = models.CharField('品牌', max_length=20, blank=True, null=True)
    ordinal = models.IntegerField('序号', blank=True, null=True, default=0)

    class Meta:
        verbose_name = u'商品'
        verbose_name_plural = u'商品'

    def __str__(self):
        return "%s , %s , %s" % (self.name, self.ename, self.help_name)

    def volume(self):
        return self.width * self.height * self.length
    volume.short_description = u'体积'

    def save(self, *args, **kwargs):
        if self.product_id is None:
            self.product_id = -1
            super(Product, self).save(*args, **kwargs)
            self.product_id = 10000000 + Product.objects.count()
            super(Product, self).save(*args, **kwargs)
        super(Product, self).save(*args, **kwargs)


@python_2_unicode_compatible
class Warehouse(models.Model):
    type_choices = (
        (u'normal', u'全品类仓库'),
        (u'blp', u'不良品仓库'),
        (u'zp', u'赠品仓库'),
    )
    wh_id = models.IntegerField('仓库编号',unique=True, help_text=u'留空系统会自动生成', blank=True)
    name = models.CharField('仓库名称', max_length=80)
    ename = models.CharField('仓库简码', max_length=4, blank=True, null=True)
    address = models.CharField('仓库地址', max_length=75, blank=True)
    type = models.CharField('仓库类型', max_length=8, choices=type_choices, default='normal')

    class Meta:
        verbose_name = u'仓库'
        verbose_name_plural = u'仓库'

    def __str__(self):
        return self.name

    def save(self , *args , **kwargs):
        if self.wh_id is None:
            self.wh_id = -1
            super(Warehouse , self).save(*args , **kwargs)
            self.wh_id = 10000 + self.id
            super(Warehouse , self).save(*args , **kwargs)
        super(Warehouse , self).save(*args , **kwargs)


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

