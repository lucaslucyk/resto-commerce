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
    readonly_fields = ['fecha', 'amount', 'preference_id'] #, 'status']
    list_display = ('fecha', 'order_type', 'amount', 'status')

    actions = ["pay_order", "update_mp_status"]

    def pay_order(self, request, queryset=None):
        return redirect('checkout', order=queryset[0].pk)

    def update_mp_status(self, request, queryset=None):
        for qs in queryset:
            qs.update_payment_status()

    update_mp_status.short_description = "Update Mercadopago Status"
    pay_order.short_description = "Pay Order"
    
