# Generated by Django 2.2.13 on 2020-07-13 20:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0007_auto_20200713_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 13, 17, 54, 12, 823919)),
        ),
    ]