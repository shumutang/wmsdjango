# -*-coding:utf-8-*-

from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from import_export.admin import ImportExportModelAdmin
from import_export import resources

from .models import Customer , Product , Location , Warehouse
from .models import OrderInProductship , OrderOutProductship , OrderOut , OrderIn

from time import time
from datetime import datetime


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        import_id_fields = ('barcode' ,)
        fields = ['customer'
            , 'name'
            , 'ename'
            , 'help_name'
            , 'batch_num'
            , 'type'
            , 'categories'
            , 'base_unit'
            , 'pcs_perunit'
            , 'Logistics_unit'
            , 'pcs_Logistics'
            , 'life_day'
            , 'price'
            , 'width'
            , 'height'
            , 'length'
            , 'weight'
            , 'net_weight'
            , 'valid_flag'
            , 'barcode'
            , 'specs'
            , 'brand'
            , 'ordinal'
                  ]


class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_per_page = 20
    list_display = ['product_id'
        , 'barcode'
        , 'name'
        , 'ename'
        , 'customer'
        , 'help_name'
        , 'batch_num'
        , 'type'
        , 'categories'
        , 'base_unit'
        , 'pcs_perunit'
        , 'Logistics_unit'
        , 'pcs_Logistics'
        , 'life_day'
        , 'price'
        , 'width' , 'height' , 'length' , 'weight' , 'volume' , 'net_weight' , 'valid_flag' ]
    fieldsets = [
        (None , {'fields': ['product_id'
            , 'name'
            , 'ename'
            , 'customer'
            , 'help_name'
            , 'pcs_Logistics'
            , 'batch_num' , 'type' , 'categories' , 'base_unit' , 'pcs_perunit' , 'barcode' , ]}) ,

        (u'包装信息' , {'fields': ['life_day'
            , 'price'
            , 'width'
            , 'height'
            , 'length'
            , 'weight'
            , 'net_weight'
            , 'valid_flag'
            , 'Logistics_unit'
            , 'specs'
            , 'brand'
            , 'ordinal'] ,
                    'classes': ['collapse']}) ,
    ]
    search_fields = ['product_id'
        , 'customer'
        , 'help_name'
        , 'name'
        , 'ename'
        , 'batch_num'
        , 'type'
        , 'barcode'
        , 'categories']
admin.site.register(Product , ProductAdmin)


class CustomerResource(resources.ModelResource):
    class Meta:
        model = Customer
        import_id_fields = ('name' ,)
        fields = ('name' , 'address' , 'city' , 'tel' , 'phone' , 'email')

class CustomerAdmin(ImportExportModelAdmin):
    resource_class = CustomerResource
    list_display = ['customer_id' , 'name' , 'address' , 'city' , 'tel' , 'phone' , 'email']
    search_fields = ['name' , 'address' , 'city' , 'tel' , 'phone' , 'email']

admin.site.register(Customer , CustomerAdmin)


class WarehouseResource(resources.ModelResource):
    class Meta:
        model = Warehouse

class WarehouseAdmin(ImportExportModelAdmin):
    resource_class = WarehouseResource
    list_display = ['wh_id' , 'name' , 'ename' , 'address' , 'type']
    search_fields = ['wh_id' , 'name' , 'ename' , 'address' , 'type' , ]
admin.site.register(Warehouse , WarehouseAdmin)


class OrderInProductshipResource(resources.ModelResource):
    class Meta:
        model = OrderInProductship
        import_id_fields = ('orderin__in_number' ,'product__barcode',)
        fields = ('orderin__in_number' , 'product__barcode', 'orderin_pcs')

class OrderInProductshipAdmin(ImportExportModelAdmin):
    resource_class = OrderInProductshipResource
    list_per_page = 20
    list_display = ['orderin'
            , 'productid'
            , 'product'
            , 'specs'
            , 'barcode'
            , 'orderin_pcs'
            , 'fact_intime' ]
    search_fields = ['orderin__in_number','product__product_id','product__barcode', 'product__specs' ]

    def barcode(self , obj):
        return obj.product.barcode
    barcode.short_description = u"条形码"

    def productid(self , obj):
        return obj.product.product_id
    productid.short_description = u'商品编码'

    def specs(self , obj):
        return obj.product.specs
    specs.short_description = u'规格'

    def fact_intime(self , obj):
        return obj.orderin.fact_in_time
    fact_intime.short_description = u'实际入库时间'

admin.site.register(OrderInProductship , OrderInProductshipAdmin)


class OrderOutProductshipResource(resources.ModelResource):
    class Meta:
        model = OrderOutProductship
        import_id_fields = ('orderout',)
        fields = ('orderout' , 'barcode' , 'orderout_pcs')

class OrderOutProductshipAdmin(ImportExportModelAdmin):
    resource_class = OrderOutProductshipResource
    list_per_page = 20
    list_display = ['orderout' , 'product' , 'barcode' , 'orderout_pcs' , ]

    def barcode(self , obj):
        return obj.product.barcode
    barcode.short_description = (u"条形码")

admin.site.register(OrderOutProductship , OrderOutProductshipAdmin)


class OrderInProductshipInline(admin.TabularInline):
    """
    fieldsets = (('' , {
        'fields': (
            'product' ,
            'barcode' ,
            'orderin_pcs' ,
        )
    }) ,)
    """
    fields = ['product', 'orderin_pcs']

    def barcode(self , obj):
        return obj.product.barcode
    barcode.short_description = (u"条形码")

    model = OrderInProductship
    extra = 5
    fk_name = 'orderin'


class OrderOutProductshipInline(admin.TabularInline):
    fieldsets = (('' , {
        'fields': (
            'product' ,
            'orderout_pcs' ,
        )
    }) ,)
    model = OrderOutProductship
    extra = 5


class OrderInResource(resources.ModelResource):
    class Meta:
        model = OrderIn
        fields = ('in_number' , 'customer' , 'pcs' , 'warehouse' , 'plan_in_time')


class OrderInAdmin(ImportExportModelAdmin):
    resource_class = OrderInResource
    list_display = ['in_number'
        , 'customer'
        , 'pcs'
        , 'boxes'
        , 'warehouse'
        , 'order_type'
        , 'order_comment'
        , 'receiver'
        , 'order_state'
        , 'in_store'
        , 'plan_in_time'
        , 'fact_in_time'
        , 'operator' ]
    search_fields = ['in_number' , 'customer__name' , 'in_store' , 'order_state' , 'product__name']
    inlines = [OrderInProductshipInline]
    fieldsets = [
        (None , {'fields': ['in_number'
            , 'warehouse'
            , 'customer'
            , 'invoice'
            , ('order_type' , 'order_state')
            , 'in_store'
            , 'plan_in_time'
            , 'fact_in_time'
            , 'order_comment']}) ,

        (u'扩展信息' , {'fields': ['serial_number'
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
        # import_id_fields = ('order_id',)


class OrderOutAdmin(ImportExportModelAdmin):
    resource_class = OrderOutResource
    list_display = ['out_number'
        , 'pcs'
        , 'boxes'
        , 'customer'
        , 'warehouse'
        , 'order_type'
        , 'order_comment'
        , 'operator'
        , 'order_state'
        , 'fact_out_time'
        , 'serial_number'
        , 'operator']
    search_fields = ['in_number' , 'customer__name' , 'order_state' , 'warehouse__ename' , ]
    inlines = [OrderOutProductshipInline]
    fieldsets = [
        (None , {'fields': ['out_number'
            , 'warehouse'
            , 'customer'
            , 'invoice'
            , ('order_type' , 'order_state')
            , 'in_store'
            , 'fact_out_time'
            , 'order_comment'
            , ]}) ,

        (u'扩展信息' , {'fields': ['serial_number'
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


class LocationResource(resources.ModelResource):
    class Meta:
        model = Location
        fields = ['location_id'
            , 'state'
            , 'type'
            , 'category'
            , 'freeze_flag'
            , 'area'
            , 'mixstore'
            , 'mixbatch'
            , 'repeate'
            , 'x'
            , 'y'
            , 'z'
            , 'valid_flag'
            , 'standcode'
            , 'up'
            , 'left'
            , 'length'
            , 'width'
            , 'volume'
            , 'comment'
            , 'help_tag'
            , 'name'
            , 'customer'
            , 'warehouse']

        import_id_fields = ('location_id' ,)


class LocationAdmin(ImportExportModelAdmin):
    resource_class = LocationResource
    list_display = ['location_id'
        , 'state'
        , 'type'
        , 'category'
        , 'freeze_flag'
        , 'area'
        , 'mixstore'
        , 'mixbatch'
        , 'repeate'
        , 'x'
        , 'y'
        , 'z'
        , 'valid_flag'
        , 'standcode'
        , 'up'
        , 'left'
        , 'length'
        , 'width'
        , 'volume'
        , 'comment'
        , 'help_tag'
        , 'name'
        , 'customer'
        , 'warehouse']
    search_fields = ['location_id' , 'state' , 'type' , 'category' , 'name']

    fieldsets = [
        (None , {'fields': ['location_id'
            , 'state'
            , 'type'
            , 'category'
            , 'freeze_flag'
            , 'area'
            , 'mixstore'
            , 'mixbatch'
            , 'repeate'
            , 'warehouse'
            , 'customer']}) ,

        (u'扩展信息' , dict(fields=[('x'
                                 , 'y'
                                 , 'z')
            , 'valid_flag'
            , 'standcode'
            , 'up'
            , 'left'
            , 'length'
            , 'width'
            , 'volume'
            , 'comment'
            , 'help_tag'
            , 'name'] , classes=['collapse'])) ,
    ]

admin.site.register(Location , LocationAdmin)
