# Generated by Django 3.2 on 2021-07-02 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0040_alter_order_ordertime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='ordered_products',
        ),
    ]
