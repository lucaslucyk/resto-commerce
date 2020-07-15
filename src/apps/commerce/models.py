from django.db import models
from django.conf import settings
from apps.resto import models as resto_models
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal

from datetime import datetime

from utils import mercadopago

# Create your models here.
class Order(models.Model):
    fecha = models.DateTimeField(default=datetime.now())
    branch = models.ForeignKey(
        resto_models.Branch, on_delete=models.CASCADE, null=True, blank=True)
    order_type = models.CharField(
        choices=settings.ORDER_TYPES,
        blank=True,
        max_length=10,
        default=settings.ORDER_TYPES[0][0],
    )

    status = models.CharField(
        choices=settings.ESTADOS,
        blank=True,
        max_length=10,
        default=settings.ESTADOS[0][0],
        )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.0000'))],
        default=0.0,
    )

    preference_id = models.CharField(max_length=200, null=True, blank=True)

    def save(self, *args, **kwargs):
        """ Set hours attributes with start and end properties. """
        self.amount = self.calc_amount()
        super().save(*args, **kwargs)

    def calc_amount(self):
        ammounts = []
        lines = OrderLine.objects.filter(order=self)
        #lines = self.orderline_set.all()
        for line in lines:
            if line.item.use_product_price:
                ammounts.append(line.quantity * line.item.product.price)
            else:
                ammounts.append(line.quantity * line.item.custom_price)
        
        return sum(ammounts)

    def update_payment_status(self):
        """ Update status consulting payment on Mercadopago """

        # get access token 
        access_token = self.branch.restaurant.mp_access_token
        if not self.branch.use_restaurant_credentials:
            access_token = self.branch.mp_branch_access_token

        # create client
        mp = mercadopago.MP(access_token)

        # getting orders
        order_filters = {"preference_id": self.preference_id}
        orders = mp.search_order(order_filters, limit=30)

        for order in orders["response"]["elements"]:
            payment_filters = {"order.id": order.get("id")}
            payments = mp.search_payment(payment_filters, limit=30)

            if not payments["status"] == 200:
                continue
            if not payments["response"]["results"]:
                continue

            for payment in payments["response"]["results"]:
                if payment["status"] == "approved":
                    if self.amount == payment["transaction_amount"]:
                        self.status = settings.ESTADOS[1][0]
                        self.save()
                        return

    def __str__(self):
        return f'{self.fecha} ({self.get_status_display()})'

class OrderLine(models.Model):
    order = models.ForeignKey(
        "Order",
        related_name="Order",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    item = models.ForeignKey(
        resto_models.MenuLine,
        related_name="item",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity}x {self.item.product}'
    
