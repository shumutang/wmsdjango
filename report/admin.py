from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from import_export import resources

# Register your models here.

from .models import Store

class StoreResource(resources.ModelResource):
    class Meta:
        model = Store

class StoreAdmin(ImportExportModelAdmin):
    resource_class = StoreResource
    list_display = ['product_id'
    ]
    search_fields = ['product' ]



admin.site.register(Store , StoreAdmin)