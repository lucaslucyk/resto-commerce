from django.contrib import admin
from apps.resto import models, forms
# Register your models here.

@admin.register(models.Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    search_fields = [
        'name',
    ]

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = [
        'name',
    ]

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = [
        'name', 'category__name',
    ]
    autocomplete_fields = ["restaurant", "category", ]

@admin.register(models.MenuLine)
class MenuLineAdmin(admin.ModelAdmin):
    search_fields = [
        'product__name', 'product__category__name',
    ]

class MenuInLine(admin.StackedInline):  # , DynamicRawIDMixin):
    model = models.MenuLine
    extra = 1
    ordering = ("product__category__name",)
    #raw_id_fields = ("producto",)
    autocomplete_fields = ["product"]
    #dynamic_raw_id_fields = ('producto',)


@admin.register(models.Menu)
class MenuAdmin(admin.ModelAdmin):
    inlines = [MenuInLine, ]
    autocomplete_fields = ["branch", ]


@admin.register(models.Branch)
class BranchAdmin(admin.ModelAdmin):
    search_fields = [
        'name', 'restaurant__name',
    ]
    autocomplete_fields = ["restaurant", ]
