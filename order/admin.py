# -*-coding:utf-8-*-

from __future__ import unicode_literals

from django.contrib import admin

from time import time
from datetime import datetime

from import_export.admin import ImportExportModelAdmin
from import_export import resources

from .models import OrderInProductship , OrderOutProductship , OrderOut , OrderIn

admin.site.disable_action('delete_selected')

class OrderInProductshipInline(admin.TabularInline):
    fields = ['product', 'specs', 'barcode', 'productid', 'orderin_pcs',]
    readonly_fields = ['specs', 'barcode', 'productid',]

    def barcode(self , obj):
        return obj.product.barcode
    barcode.short_description = u"条形码"

    def productid(self , obj):
        return obj.product.product_id
    productid.short_description = u'商品编码'

    def specs(self , obj):
        return obj.product.specs
    specs.short_description = u'规格'

    model = OrderInProductship
    extra = 5
    fk_name = 'orderin'
    raw_id_fields = ['product']

class OrderOutProductshipInline(admin.TabularInline):
    fields = ['product', 'specs', 'barcode', 'productid', 'orderout_pcs', ]
    readonly_fields = ['specs', 'barcode', 'productid', ]

    def barcode(self, obj):
        return obj.product.barcode
    barcode.short_description = u"条形码"

    def productid(self, obj):
        return obj.product.product_id
    productid.short_description = u'商品编码'

    def specs(self, obj):
        return obj.product.specs
    specs.short_description = u'规格'

    model = OrderOutProductship
    extra = 5


class OrderInResource(resources.ModelResource):
    class Meta:
        model = OrderIn
        fields = ('in_number' , 'customer' , 'warehouse' , 'plan_in_time')


class OrderInAdmin(ImportExportModelAdmin):
    resource_class = OrderInResource
    list_display = ['id'
        , 'in_number'
        , 'customer'
        , 'warehouse'
        , 'order_type'
        , 'order_comment'
        , 'serial_number'
        , 'order_state'
        , 'in_store'
        , 'plan_in_time'
        , 'fact_in_time'
        , 'operator'
        , 'operate_date']
    search_fields = ['in_number' , 'customer__name' , 'in_store' , 'order_state' , 'product__name']
    list_display_links = ['in_number']
    inlines = [OrderInProductshipInline]
    fieldsets = [
        (None , {'fields': ['in_number'
            , 'warehouse'
            , 'customer'
            , ('order_type' , 'order_state')
            , 'in_store'
            , 'plan_in_time'
            , 'fact_in_time'
            , 'order_comment']}) ,

        (u'扩展信息' , {'fields': ['serial_number'
            , 'invoice'
            , 'sender'
            , 'pcs'
            , 'boxes'
            , 'receiver'
            , 'operator'] ,
                    'classes': ['collapse']}) ,
    ]


    def save_model(self , request , obj , form , change):
        if not change:
            ts = int(time())
            now = datetime.now()
            nowstr = now.strftime('%Y%m%d%H%M%S')
            obj.in_number = "in%s" % ts
            obj.serial_number = "%s%s" % (obj.order_type , nowstr)
            obj.operator = request.user.username
        super(OrderInAdmin , self).save_model(request , obj , form , change)
admin.site.register(OrderIn , OrderInAdmin)


class OrderOutResource(resources.ModelResource):
    class Meta:
        model = OrderOut

class OrderOutAdmin(ImportExportModelAdmin):
    resource_class = OrderOutResource
    list_display = ['out_number'
        , 'customer'
        , 'warehouse'
        , 'order_type'
        , 'order_comment'
        , 'operator'
        , 'order_state'
        , 'out_store'
        , 'fact_out_time'
        , 'serial_number'
        , 'operator'
        , 'operate_date']
    search_fields = ['in_number' , 'customer__name' , 'order_state' , 'warehouse__ename' , ]
    inlines = [OrderOutProductshipInline]
    fieldsets = [
        (None , {'fields': ['out_number'
            , 'warehouse'
            , 'customer'
            , ('order_type' , 'order_state')
            , 'out_store'
            , 'fact_out_time'
            , 'order_comment'
            , ]}) ,

        (u'扩展信息' , {'fields': ['serial_number'
            , 'invoice'
            , 'pcs'
            , 'boxes'
            , ('receiver' , 'receiver_addr' , 'receiver_phone')
            , 'operator'] ,
                    'classes': ['collapse']}) ,
    ]

    def save_model(self , request , obj , form , change):
        if not change:
            ts = int(time())
            now = datetime.now()
            nowstr = now.strftime('%Y%m%d%H%M%S')
            obj.out_number = "out%s" % ts
            obj.serial_number = "%s%s" % (obj.order_type , nowstr)
            obj.operator = request.user.username
        super(OrderOutAdmin , self).save_model(request , obj , form , change)

admin.site.register(OrderOut , OrderOutAdmin)


class OrderInProductshipResource(resources.ModelResource):
    class Meta:
        model = OrderInProductship

class OrderInProductshipAdmin(ImportExportModelAdmin):
    resource_class = OrderInProductshipResource
    list_per_page = 20
    list_display = ['id'
            , 'orderin'
            , 'productcode'
            , 'product'
            , 'specs'
            , 'barcode'
            , 'instore'
            , 'orderin_pcs'
            , 'plan_intime'
            , 'fact_intime'
            , 'operate_time'
    ]
    search_fields = ['orderin__in_number','product__product_id','product__barcode', 'product__specs' ]
    list_filter = ['orderin__in_store', 'orderin__operate_date', 'orderin__fact_in_time']
    actions = None
    raw_id_fields = ['product']
    view_on_site = False
    list_display_links = None

    def orderinid(self, obj):
        return obj.orderin.id
    orderinid.short_description = u"订单id"

    def productid(self, obj):
        return obj.product.id
    productid.short_description = u"商品id"

    def barcode(self , obj):
        return obj.product.barcode
    barcode.short_description = u"条形码"

    def productcode(self , obj):
        return obj.product.product_id
    productcode.short_description = u'商品编码'

    def specs(self , obj):
        return obj.product.specs
    specs.short_description = u'规格'

    def plan_intime(self , obj):
        return obj.orderin.plan_in_time
    plan_intime.short_description = u'计划入库日期'

    def fact_intime(self , obj):
        return obj.orderin.fact_in_time
    fact_intime.short_description = u'实际入库日期'

    def operate_time(self , obj):
        return obj.orderin.operate_date
    operate_time.short_description = u'操作日期'

    def instore(self , obj):
        return u'已完成' if obj.orderin.in_store == 'y' else u'未完成'
    instore.short_description = u'入库'

admin.site.register(OrderInProductship , OrderInProductshipAdmin)


class OrderOutProductshipResource(resources.ModelResource):
    class Meta:
        model = OrderOutProductship

class OrderOutProductshipAdmin(ImportExportModelAdmin):
    resource_class = OrderOutProductshipResource
    list_per_page = 20
    list_display = ['orderout'
        , 'productcode'
        , 'product'
        , 'specs'
        , 'barcode'
        , 'orderout_pcs'
        , 'outstore'
        , 'fact_outtime'
        , 'operate_time'
    ]
    search_fields = ['orderout__out_number', 'product__product_id', 'product__barcode', 'product__specs']
    list_filter = ['orderout__out_store', 'orderout__operate_date', 'orderout__fact_out_time']
    actions = None
    view_on_site = False
    list_display_links = None

    def barcode(self, obj):
        return obj.product.barcode
    barcode.short_description = u"条形码"

    def productcode(self, obj):
        return obj.product.product_id
    productcode.short_description = u'商品编码'

    def specs(self, obj):
        return obj.product.specs
    specs.short_description = u'规格'

    def fact_outtime(self, obj):
        return obj.orderout.fact_out_time
    fact_outtime.short_description = u'实际出库日期'

    def operate_time(self, obj):
        return obj.orderout.operate_date
    operate_time.short_description = u'操作日期'

    def outstore(self, obj):
        return u'已完成' if obj.orderout.out_store == 'y' else u'未完成'
    outstore.short_description = u'出库'

admin.site.register(OrderOutProductship , OrderOutProductshipAdmin)
