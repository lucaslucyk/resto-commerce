# Generated by Django 2.2.13 on 2020-07-13 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0003_order_preference_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='estado',
            new_name='status',
        ),
    ]