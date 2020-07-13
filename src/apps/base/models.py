### django ###
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal

#from apps.resto import models as resto_models


# Create your models here.
class Licensing(models.Model):
    name = models.CharField(max_length=100)
    restaurants = models.PositiveIntegerField(blank=True, null=True)
    branches = models.PositiveIntegerField(blank=True, null=True)
    menus = models.PositiveIntegerField(blank=True, null=True)
    products = models.PositiveIntegerField(blank=True, null=True)

    order_instead = models.BooleanField(blank=True, null=True)
    order_take_away = models.BooleanField(blank=True, null=True)
    order_delivery = models.BooleanField(blank=True, null=True)

    payment_gateway = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return self.name


class Plan(models.Model):
    licensing = models.ForeignKey(Licensing, null=True, on_delete=models.CASCADE)
    duration = models.PositiveIntegerField(default=1, help_text="Months")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        #dafault=0.0,
    )

    def __str__(self):
        return f'{self.licensing} for {self.duration} month/s'


class Profile(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, null=True, on_delete=models.SET_NULL)
    expiration = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return f'{self.user}, {self.plan}. Expires: {self.expiration}'
    

    

