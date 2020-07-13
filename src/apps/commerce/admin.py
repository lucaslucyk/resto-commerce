from django.contrib import admin
from apps.commerce import models
from django.shortcuts import redirect

# Register your models here.

@admin.register(models.OrderLine)
class OrderLineAdmin(admin.ModelAdmin):
    search_fields = [
        'item__product__name', 'item__product__category__name',
    ]

class OrderInLine(admin.StackedInline):  # , DynamicRawIDMixin):
    model = models.OrderLine
    extra = 1
    ordering = ("item__product__category__name",)
    #raw_id_fields = ("producto",)
    autocomplete_fields = ["item"]
    #dynamic_raw_id_fields = ('producto',)

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderInLine, ]
    autocomplete_fields = ["branch", ]
    readonly_fields = ['fecha', 'status', 'amount', 'preference_id']

    actions = ["pay_order"]

    def pay_order(self, request, queryset=None):
        return redirect('checkout', order=queryset[0].pk)

    pay_order.short_description = "Pay Order"
    
