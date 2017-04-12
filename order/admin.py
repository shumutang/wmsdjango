# -*-coding:utf-8-*-

from __future__ import unicode_literals

from django.contrib import admin
from django import forms
from django.forms import ModelForm
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.contrib.admin.widgets import ManyToManyRawIdWidget

from django.db.models import Count, Sum

from time import time
from datetime import datetime

from django.urls import reverse
from django.shortcuts import render

from import_export.admin import ImportExportModelAdmin
from import_export import resources

from .models import OrderInProductship, OrderOutProductship, OrderOut, OrderIn

admin.site.disable_action('delete_selected')


class OrderInProductshipForm(forms.ModelForm):
    class Meta:
        model = OrderInProductship
        fields = '__all__'
        widgets = {
            'product': ForeignKeyRawIdWidget(OrderInProductship._meta.get_field("product").rel,
                                             admin.site,
                                             attrs={'size': '40'}),
            'orderin_pcs': forms.TextInput(attrs={'size': '10'}),
        }

class OrderInProductshipInline(admin.TabularInline):
    fields = ['product', 'barcode', 'specs', 'productid', 'orderin_pcs', ]
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

    model = OrderInProductship
    extra = 5
    fk_name = 'orderin'
    #raw_id_fields = ['product']
    form = OrderInProductshipForm

class OrderOutProductshipInline(admin.TabularInline):
    fields = ['product', 'barcode', 'specs', 'productid', 'store', 'orderout_pcs', ]
    readonly_fields = ['specs', 'barcode', 'productid', 'store']

    def barcode(self, obj):
        return obj.product.barcode

    barcode.short_description = u"条形码"

    def productid(self, obj):
        return obj.product.product_id

    productid.short_description = u'商品编码'

    def specs(self, obj):
        return obj.product.specs

    specs.short_description = u'规格'

    def store(self, obj):
        barcode = obj.product.barcode
        instore = OrderInProductship.objects.filter(
            product=barcode
            , orderin__in_store='y').aggregate(Sum('orderin_pcs'))
        outstore = OrderOutProductship.objects.filter(
            product=barcode
            , orderout__out_store='y').aggregate(Sum('orderout_pcs'))
        instore_pcs = 0 if instore['orderin_pcs__sum'] == None else instore['orderin_pcs__sum']
        outstore_pcs = 0 if outstore['orderout_pcs__sum'] == None else outstore['orderout_pcs__sum']
        return instore_pcs - outstore_pcs
    store.short_description = u'库存'

    model = OrderOutProductship
    extra = 5
    fk_name = 'orderout'
    raw_id_fields = ['product']

class OrderInResource(resources.ModelResource):
    class Meta:
        model = OrderIn
        fields = ('in_number', 'customer', 'warehouse', 'plan_in_time')


class OrderInAdmin(ImportExportModelAdmin):
    resource_class = OrderInResource
    readonly_fields = ['in_store', ]
    list_display = ['in_number'
        , 'customer'
        , 'warehouse'
        , 'order_type'
        , 'order_comment'
        , 'serial_number'
        , 'in_store'
        , 'plan_in_time'
        , 'fact_in_time'
        , 'operator'
        , 'operate_date']
    search_fields = ['in_number', 'customer__name', 'in_store', 'product__name']
    list_display_links = ['in_number']
    inlines = [OrderInProductshipInline]
    fieldsets = [
        (None, {'fields': ['in_number'
            , 'warehouse'
            , 'customer'
            , 'order_type'
            , 'in_store'
            , 'plan_in_time'
            , 'fact_in_time'
            , 'order_comment']}),

        (u'扩展信息', {'fields': ['serial_number'
            , 'invoice'
            , 'sender'
            , 'pcs'
            , 'boxes'
            , 'receiver'
            , 'operator'],
                   'classes': ['collapse']}),
    ]

    # radio_fields = {"in_store": admin.HORIZONTAL}
    # radio_fields = {"in_store": admin.VERTICAL}
    actions = ['make_instore', 'print_instore_detail']


    def make_instore(self, request, queryset):
        for order in queryset:
            if order.in_store == 'n':
                order.in_store = 'y'
                order.save()
                msg = u'订单(%s) 完成入库确认' % order.in_number
            elif order.in_store == 'y':
                msg = u'订单(%s) 已入库完成，不需重复确认入库' % order.in_number
            else:
                msg = u'订单(%s) 确认入库异常' % order.in_number
            self.message_user(request, msg)
    make_instore.short_description = u"确认入库"

    def print_instore_detail(self, request, queryset):
        for order in queryset:
            in_number = order.in_number
            context = {'order_product_list': OrderInProductship.objects.filter(orderin=in_number)}
            return render(request, 'order/indetail.html', context)
    print_instore_detail.short_description = u"打印入库单"

    def save_model(self, request, obj, form, change):
        if change:
            obj_old = self.model.objects.get(pk=obj.pk)
            if obj_old.in_store == 'y':
                Msg = u'已完成订单，不能被修改'
                self.message_user(request, Msg, 40)
            else:
                super(OrderInAdmin, self).save_model(request, obj, form, change)
        else:
            ts = int(time())
            now = datetime.now()
            nowstr = now.strftime('%Y%m%d%H%M%S')
            if not obj.in_number:
                obj.in_number = "in%s" % ts
            obj.serial_number = "%s%s" % (obj.order_type, nowstr)
            obj.operator = request.user.username
            super(OrderInAdmin, self).save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        orderout = form.instance
        instances = formset.save(commit=False)
        for instance in instances:
            if change and orderout.in_store == 'y':
                Msg = u'已完成订单，不能被修改'
                self.message_user(request, Msg, 40)
            else:
                super(OrderInAdmin, self).save_formset(request, form, formset, change)

    def delete_model(self, request, obj):
        if obj.in_store == 'y':
            Msg = u'已完成订单，不能被删除'
            self.message_user(request, Msg, 40)
        else:
            super(OrderInAdmin, self).delete_model(request, obj)

    def response_change(self, request, obj):
        if obj.in_store == 'y':
            return self.response_post_save_change(request, obj)
        else:
            super(OrderInAdmin, self).response_change(request, obj)
            return self.response_post_save_change(request, obj)

    def response_delete(self, request, obj_display, obj_id):
        obj_old = self.model.objects.get(pk=obj_id)
        post_url = reverse('admin:index', current_app=self.admin_site.name)
        if obj_old.in_store == 'y':
            return self.response_post_save_change(request, obj_old)
        else:
            super(OrderInAdmin, self).response_delete(request, obj_display, obj_id)
            return self.response_post_save_change(request, obj_old)

admin.site.register(OrderIn, OrderInAdmin)


class OrderOutResource(resources.ModelResource):
    class Meta:
        model = OrderOut

class OrderOutAdmin(ImportExportModelAdmin):
    resource_class = OrderOutResource
    readonly_fields = ['out_store', ]
    list_display = ['out_number'
        , 'customer'
        , 'warehouse'
        , 'order_type'
        , 'order_comment'
        , 'operator'
        , 'out_store'
        , 'fact_out_time'
        , 'serial_number'
        , 'operator'
        , 'operate_date']
    search_fields = ['in_number', 'customer__name', 'warehouse__ename', ]
    inlines = [OrderOutProductshipInline]
    fieldsets = [
        (None, {'fields': ['out_number'
            , 'warehouse'
            , 'customer'
            , 'order_type'
            , 'out_store'
            , 'fact_out_time'
            , 'order_comment'
            , ]}),

        (u'扩展信息', {'fields': ['serial_number'
            , 'invoice'
            , 'pcs'
            , 'boxes'
            , ('receiver', 'receiver_addr', 'receiver_phone')
            , 'operator'],
                   'classes': ['collapse']}),
    ]
    radio_fields = {"out_store": admin.VERTICAL}
    actions = ['make_outstore','print_outstore_detail']

    def make_outstore(self, request, queryset):
        for order in queryset:
            if order.out_store == 'n':
                order.out_store = 'y'
                order.save()
                msg = u'订单(%s) 完成出库确认' % order.out_number
            elif order.out_store == 'y':
                msg = u'订单(%s) 已出库完成，不需重复确认出库' % order.out_number
            else:
                msg = u'订单(%s) 确认出库异常' % order.out_number
            self.message_user(request, msg)
    make_outstore.short_description = u"确认出库"

    def print_outstore_detail(self, request, queryset):
        for order in queryset:
            out_number = order.out_number
            context = {'order_product_list': OrderOutProductship.objects.filter(orderout=out_number)}
            return render(request, 'order/outdetail.html', context)
    print_outstore_detail.short_description = u"打印出库单"

    def save_model(self, request, obj, form, change):
        if change:
            obj_old = self.model.objects.get(pk=obj.pk)
            if obj_old.out_store == 'y':
                Msg = u'已完成订单，不能被修改'
                self.message_user(request, Msg, 40)
            else:
                super(OrderOutAdmin, self).save_model(request, obj, form, change)
        else:
            ts = int(time())
            now = datetime.now()
            nowstr = now.strftime('%Y%m%d%H%M%S')
            if not obj.out_number:
                obj.out_number = "out%s" % ts
            obj.serial_number = "%s%s" % (obj.order_type, nowstr)
            obj.operator = request.user.username
            super(OrderOutAdmin, self).save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        orderout = form.instance
        instances = formset.save(commit=False)
        for instance in instances:
            if change and orderout.out_store == 'y':
                Msg = u'已完成订单，不能被修改'
                self.message_user(request, Msg, 40)
            else:
                super(OrderOutAdmin, self).save_formset(request, form, formset, change)

    def delete_model(self, request, obj):
        if obj.out_store == 'y':
            Msg = u'已完成订单，不能被删除'
            self.message_user(request, Msg, 40)
            # messages.add_message(request, messages.ERROR, Msg)
        else:
            super(OrderOutAdmin, self).delete_model(request, obj)

    def response_change(self, request, obj):
        if obj.out_store == 'y':
            return self.response_post_save_change(request, obj)
        else:
            super(OrderOutAdmin, self).response_change(request, obj)
            return self.response_post_save_change(request, obj)

    def response_delete(self, request, obj_display, obj_id):
        obj_old = self.model.objects.get(pk=obj_id)
        post_url = reverse('admin:index', current_app=self.admin_site.name)
        if obj_old.out_store == 'y':
            return self.response_post_save_change(request, obj_old)
        else:
            super(OrderOutAdmin, self).response_delete(request, obj_display, obj_id)
            return self.response_post_save_change(request, obj_old)

admin.site.register(OrderOut, OrderOutAdmin)


class OrderInProductshipResource(resources.ModelResource):
    class Meta:
        model = OrderInProductship

class OrderInProductshipAdmin(admin.ModelAdmin):
    resource_class = OrderInProductshipResource
    list_per_page = 20
    list_display = ['id'
        , 'innumber'
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
    search_fields = ['orderin__in_number'
        , 'product__product_id'
        , 'product__barcode'
        , 'product__specs'
    ]
    list_filter = ['orderin__in_store'
        , 'orderin__operate_date'
        , 'orderin__fact_in_time'
    ]
    actions = None
    # raw_id_fields = ['product']
    view_on_site = False
    list_display_links = ['id','barcode',]

    def barcode(self, obj):
        result = '<a href="%s%s">%s</a> ' % ('../../wms/product/', obj.product.barcode, obj.product.barcode)
        return result
    barcode.allow_tags = True
    barcode.short_description = u"条形码"

    def innumber(self, obj):
        result = '<a href="%s%s">%s</a> ' % ('../orderin/', obj.orderin.in_number, obj.orderin.in_number,)
        return result
    innumber.allow_tags = True
    innumber.short_description = u"入库编号"

    def productcode(self, obj):
        return obj.product.product_id

    productcode.short_description = u'商品编码'

    def specs(self, obj):
        return obj.product.specs

    specs.short_description = u'规格'

    def plan_intime(self, obj):
        return obj.orderin.plan_in_time

    plan_intime.short_description = u'计划入库日期'

    def fact_intime(self, obj):
        return obj.orderin.fact_in_time

    fact_intime.short_description = u'实际入库日期'

    def operate_time(self, obj):
        return obj.orderin.operate_date

    operate_time.short_description = u'操作日期'

    def instore(self, obj):
        return u'已完成' if obj.orderin.in_store == 'y' else u'未完成'

    instore.short_description = u'入库'

    def save_model(self, request, obj, form, change):
        if change:
            obj_old = self.model.objects.get(pk=obj.pk)
            if obj_old.orderin.in_store == 'y':
                Msg = u'已完成订单，不能被修改'
                self.message_user(request, Msg, 40)
            else:
                super(OrderInProductshipAdmin, self).save_model(request, obj, form, change)
        else:
            super(OrderInProductshipAdmin, self).save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        if obj.orderin.in_store == 'y':
            Msg = u'已完成订单，不能被删除'
            self.message_user(request, Msg, 40)
        else:
            super(OrderInProductshipAdmin, self).delete_model(request, obj)

    def response_change(self, request, obj):
        if obj.orderin.in_store == 'y':
            Msg = u'已完成订单，不能被删除'
            # messages.add_message(request, messages.ERROR, Msg)
            return self.response_post_save_change(request, obj)
        else:
            super(OrderInProductshipAdmin, self).response_change(request, obj)
            return self.response_post_save_change(request, obj)

    def response_delete(self, request, obj_display, obj_id):
        obj_old = self.model.objects.get(pk=obj_id)
        post_url = reverse('admin:index', current_app=self.admin_site.name)
        if obj_old.orderin.in_store == 'y':
            return self.response_post_save_change(request, obj_old)
        else:
            super(OrderInProductshipAdmin, self).response_delete(request, obj_display, obj_id)
            return self.response_post_save_change(request, obj_old)

admin.site.register(OrderInProductship, OrderInProductshipAdmin)


class OrderOutProductshipResource(resources.ModelResource):
    class Meta:
        model = OrderOutProductship


class OrderOutProductshipAdmin(ImportExportModelAdmin):
    resource_class = OrderOutProductshipResource
    list_per_page = 20
    list_display = ['id'
        , 'outnumber'
        , 'productcode'
        , 'product'
        , 'specs'
        , 'barcode'
        , 'orderout_pcs'
        , 'outstore'
        , 'fact_outtime'
        , 'operate_time'
    ]
    search_fields = ['orderout__out_number'
        , 'product__product_id'
        , 'product__barcode'
        , 'product__specs'
    ]
    list_filter = ['orderout__out_store'
        , 'orderout__operate_date'
        , 'orderout__fact_out_time'
    ]
    actions = None
    # raw_id_fields = ['product']
    view_on_site = False
    list_display_links = ['id', 'barcode', 'outnumber']

    def barcode(self, obj):
        result = '<a href="%s%s">%s</a> ' % ('../../wms/product/', obj.product.barcode, obj.product.barcode)
        return result
    barcode.allow_tags = True
    barcode.short_description = u"条形码"

    def outnumber(self, obj):
        result = '<a href="%s%s">%s</a> ' % ('../orderout/', obj.orderout.out_number, obj.orderout.out_number,)
        return result
    outnumber.allow_tags = True
    outnumber.short_description = u"出库编号"

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

    def save_model(self, request, obj, form, change):
        if change:
            obj_old = self.model.objects.get(pk=obj.pk)
            if obj_old.orderout.out_store == 'y':
                Msg = u'已完成订单，不能被修改'
                self.message_user(request, Msg, 40)
            else:
                super(OrderOutProductshipAdmin, self).save_model(request, obj, form, change)
        else:
            super(OrderOutProductshipAdmin, self).save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        if obj.orderout.out_store == 'y':
            Msg = u'已完成订单，不能被删除'
            self.message_user(request, Msg, 40)
        else:
            super(OrderOutProductshipAdmin, self).delete_model(request, obj)

    def response_change(self, request, obj):
        if obj.orderout.out_store == 'y':
            return self.response_post_save_change(request, obj)
        else:
            super(OrderOutProductshipAdmin, self).response_change(request, obj)
            return self.response_post_save_change(request, obj)

    def response_delete(self, request, obj_display, obj_id):
        obj_old = self.model.objects.get(pk=obj_id)
        post_url = reverse('admin:index', current_app=self.admin_site.name)
        if obj_old.orderout.out_store == 'y':
            # Msg = u'已完成订单，不能被删除'
            # messages.add_message(request, messages.ERROR, Msg)
            # return HttpResponseRedirect(post_url)
            return self.response_post_save_change(request, obj_old)
        else:
            super(OrderOutProductshipAdmin, self).response_delete(request, obj_display, obj_id)
            return self.response_post_save_change(request, obj_old)

admin.site.register(OrderOutProductship, OrderOutProductshipAdmin)
