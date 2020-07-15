from utils import mercadopago

from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings

#from apps.commerce import credentials
from apps.commerce import models as commerce_models
from apps.resto import models as resto_models

# Create your views here.


def checkout(request, order, context=None):

    template = 'apps/commerce/checkout.html'
    order = commerce_models.Order.objects.get(pk=order)

    access_token = order.branch.restaurant.mp_access_token
    if not order.branch.use_restaurant_credentials:
        access_token = order.branch.mp_branch_access_token

    mp = mercadopago.MP(access_token)

    lines = commerce_models.OrderLine.objects.filter(order=order)
    items = []
    for line in lines:
        item_price = float(line.item.product.price)
        if not line.item.use_product_price:
            item_price = float(line.item.custom_price)
        items.append({
            "title": line.item.product.name,
            "quantity": line.quantity,
            "currency_id": "ARS",
            "unit_price": item_price
        })

    preference = {
        "items": items,
    }

    prefer = mp.create_preference(preference)

    #update order
    order.preference_id = prefer["response"]["id"]
    order.save()

    context = {
        "order": order.pk,
        "preference": prefer["response"]["id"],
    }

    return render(request, template, context)


def mp_callback(request, order, context=None):

    if request.method != "POST":
        return JsonResponse({"success": False})

    order = commerce_models.Order.objects.get(pk=order)

    access_token = order.branch.restaurant.mp_access_token
    if not order.branch.use_restaurant_credentials:
        access_token = order.branch.mp_branch_access_token

    mp = mercadopago.MP(access_token)

    payment = mp.get_payment(request.POST.get("payment_id"))
    preference = mp.get_preference(request.POST.get("preference_id"))

    #bad token
    if preference["response"]["id"] != order.preference_id:
        return JsonResponse({"success": False})
    
    #update order status
    if payment["response"]["status"] == "approved":
        order.status = settings.ESTADOS[1][0]
        order.save()

    return JsonResponse({
        "payment-status": payment["response"]["status"],
        "payment-detail": payment["response"]["status_detail"],
        "cardholder": payment["response"]["card"]["cardholder"],
        "payment-amount": float(payment["response"]["transaction_amount"]),
        
        "order-ammoount": float(order.amount),
        "order-items": preference["response"]["items"],
    })
