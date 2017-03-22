# -*-coding:utf-8-*-

from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from import_export.admin import ImportExportModelAdmin

# from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter

from import_export import resources
from .models import Customer, Product, Location, Warehouse
from .models import OrderInProductship, OrderOutProductship, OrderOut, OrderIn


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        import_id_fields = ('product_id',)


class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = ['product_id'
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
        , 'width', 'height', 'length', 'weight', 'volume', 'net_weight', 'valid_flag', 'barcode']

    fieldsets = [
        (None, {'fields': ['product_id'
            , 'name'
            , 'ename'
            , 'customer'
            , 'help_name'
            , 'pcs_Logistics'
            , 'batch_num', 'type', 'categories', 'base_unit', 'pcs_perunit', 'barcode', ]}),

        (u'包装信息', {'fields': ['life_day'
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
            , 'ordinal'],
                   'classes': ['collapse']}),
    ]
    search_fields = ['product_id', 'customer', 'help_name', 'name', 'ename', 'batch_num', 'type']
    list_filter = [
        # for ordinary fields
        'name',
        'ename',
        'help_name',
        'batch_num',
        'categories',
        'valid_flag',
        'customer'
    ]


admin.site.register(Product, ProductAdmin)


class CustomerResource(resources.ModelResource):
    class Meta:
        model = Customer
        import_id_fields = ('name',)
        fields = ('name', 'address', 'city', 'tel', 'phone', 'email')


class CustomerAdmin(ImportExportModelAdmin):
    resource_class = CustomerResource
    list_display = ['name', 'address', 'city', 'tel', 'phone', 'email']
    search_fields = ['name', 'address', 'city', 'tel', 'phone', 'email']
    list_filter = [
        # for ordinary fields
        'name',
        'address',
        'tel',
        'phone',
    ]


admin.site.register(Customer, CustomerAdmin)


class WarehouseResource(resources.ModelResource):
    class Meta:
        model = Warehouse


class WarehouseAdmin(ImportExportModelAdmin):
    resource_class = WarehouseResource
    list_display = ['name', 'ename', 'address', 'type']
    search_fields = ['name', 'ename', 'address', 'type', ]


admin.site.register(Warehouse, WarehouseAdmin)


class OrderInProductshipResource(resources.ModelResource):
    class Meta:
        model = OrderInProductship
        # import_id_fields = ('orderin',)


class OrderInProductshipAdmin(ImportExportModelAdmin):
    resource_class = OrderInProductshipResource
    list_display = ['orderin', 'product', 'barcode', 'orderin_pcs', ]

    def barcode(self, obj):
        return obj.product.barcode

    barcode.short_description = (u"条形码")


admin.site.register(OrderInProductship, OrderInProductshipAdmin)


class OrderOutProductshipResource(resources.ModelResource):
    class Meta:
        model = OrderOutProductship
        # import_id_fields = ('orderin',)


class OrderOutProductshipAdmin(ImportExportModelAdmin):
    resource_class = OrderOutProductshipResource
    list_display = ['orderout', 'product', 'barcode', 'orderout_pcs', ]

    def barcode(self, obj):
        return obj.product.barcode

    barcode.short_description = (u"条形码")


admin.site.register(OrderOutProductship, OrderOutProductshipAdmin)


class OrderInProductshipInline(admin.TabularInline):
    fieldsets = (('', {
        'fields': (
            'product',
            'orderin_pcs',
        )
    }),)
    model = OrderInProductship
    extra = 5


class OrderOutProductshipInline(admin.TabularInline):
    fieldsets = (('', {
        'fields': (
            'product',
            'orderout_pcs',
        )
    }),)
    model = OrderOutProductship
    extra = 5


class OrderInResource(resources.ModelResource):
    class Meta:
        model = OrderIn
        fields = ('in_number', 'customer', 'pcs', 'warehouse', 'plan_in_time')


class OrderInAdmin(ImportExportModelAdmin):
    resource_class = OrderInResource
    list_display = ['in_number'
        , 'customer'
        , 'pcs'
        , 'warehouse'
        , 'order_type'
        , 'order_comment'
        , 'operator'
        , 'order_state'
        , 'in_store'
        , 'plan_in_time']
    search_fields = ['in_number', 'customer__name', 'in_store', 'order_state', 'product__name']
    list_filter = [
        # for ordinary fields
        'customer__name',
        'order_state',
        'in_store',
        'warehouse__name',
        'order_type',
        'operate_date',
        'product',
    ]
    inlines = [OrderInProductshipInline]
    fieldsets = [
        (None, {'fields': ['in_number'
            , 'warehouse'
            , 'customer'
            , 'invoice'
            , 'pcs'
            , 'boxes'
            , ('order_type', 'order_state'), 'in_store', 'plan_in_time']}),

        (u'扩展信息', {'fields': ['sender'
            , 'serial_number'
            , 'order_comment'
            , 'receiver'
            , 'operator'
            , 'fact_in_time'],
                   'classes': ['collapse']}),
    ]


admin.site.register(OrderIn, OrderInAdmin)


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
        , 'order_state']
    search_fields = ['in_number', 'customer__name', 'order_state', 'warehouse__ename', ]
    list_filter = [
        # for ordinary fields
        'customer__name',
        'order_state',
        'warehouse__ename',
        'order_type',
        'operate_date',
    ]
    inlines = [OrderOutProductshipInline]
    fieldsets = [
        (None, {'fields': ['out_number'
            , 'warehouse'
            , 'customer'
            , 'invoice'
            , 'pcs'
            , 'boxes'
            , ('order_type', 'order_state')
            , 'in_store'
            , 'fact_out_time']}),

        (u'扩展信息', {'fields': ['serial_number'
            , ('receiver', 'receiver_addr', 'receiver_phone')
            , ('order_comment', 'operator')],
                   'classes': ['collapse']}),
    ]


admin.site.register(OrderOut, OrderOutAdmin)


class LocationResource(resources.ModelResource):
    class Meta:
        model = Location
        import_id_fields = ('order_id',)


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
    search_fields = ['location_id', 'state', 'type', 'category', 'name']

    fieldsets = [
        (None, {'fields': ['location_id'
            , 'state'
            , 'type'
            , 'category'
            , 'freeze_flag'
            , 'area'
            , 'mixstore'
            , 'mixbatch'
            , 'repeate'
            , 'warehouse'
            , 'customer']}),

        (u'扩展信息', dict(fields=[('x'
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
            , 'name'], classes=['collapse'])),
    ]


admin.site.register(Location, LocationAdmin)

