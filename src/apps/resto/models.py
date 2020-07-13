### django ###
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal

#from apps.base import models as base_models

# Create your models here.
class Restaurant(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    business_name = models.CharField(max_length=100)
    cuit = models.PositiveIntegerField()
    website = models.URLField(max_length=200)
    logo = models.ImageField(upload_to="restaurants/", null=True, blank=True)

    slug = models.SlugField()

    ### Mercadopago Credentials
    mp_public_key = models.CharField(
        "Publick Key (Mercadopago)", max_length=200, null=True, blank=True)
    mp_access_token = models.CharField(
        "Access Token (Mercadopago)", max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name
    

class Branch(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.PositiveIntegerField()

    instead = models.BooleanField(default=True)
    take_away = models.BooleanField(default=True)
    delivery = models.BooleanField(default=True)

    ### Mercadopago Credentials
    use_restaurant_credentials = models.BooleanField(
        "Use Mercadopago Keys from Restaurant", default=True)
    mp_branch_public_key = models.CharField(
        "Publick Key (Mercadopago)", max_length=200, null=True, blank=True)
    mp_branch_access_token = models.CharField(
        "Access Token (Mercadopago)", max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="products/")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.0000'))],
        #dafault=0.0,
    )

    def __str__(self):
        return self.name


class Menu(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    branch = models.ForeignKey("Branch", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="menus/", null=True, blank=True)

    def __str__(self):
        return self.branch.name


class MenuLine(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    menu = models.ForeignKey("Menu", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    use_product_price = models.BooleanField(default=True)
    custom_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.0000'))],
        default=0.0,
    )

    def __str__(self):
        return f'{self.product.name}'
