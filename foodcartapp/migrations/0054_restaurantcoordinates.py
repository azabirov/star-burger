# Generated by Django 3.2 on 2021-07-27 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0053_order_restaurant'),
    ]

    operations = [
        migrations.CreateModel(
            name='RestaurantCoordinates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=50, verbose_name='название')),
                ('lng', models.IntegerField()),
                ('lat', models.IntegerField()),
            ],
        ),
    ]
