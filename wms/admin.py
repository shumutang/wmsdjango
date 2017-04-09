# -*-coding:utf-8-*-

from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from import_export.admin import ImportExportModelAdmin
from import_export import resources

from .models import Customer , Product , Location , Warehouse

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
    list_display = ['barcode'
        , 'product_id'
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
    list_display_links = ['barcode']
    fieldsets = [
        (None , {'fields': ['barcode'
            , 'product_id'
            , 'name'
            , 'ename'
            , 'customer'
            , 'help_name'
            , 'pcs_Logistics'
            , 'batch_num' , 'type' , 'categories' , 'base_unit' , 'pcs_perunit' ,]}) ,

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
        , 'help_name'
        , 'name'
        , 'ename'
        , 'batch_num'
        , 'customer__name'
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
