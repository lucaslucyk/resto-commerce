# Generated by Django 2.2.13 on 2020-07-13 17:57

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resto', '0002_auto_20200712_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuline',
            name='custom_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.0000'))]),
        ),
    ]
