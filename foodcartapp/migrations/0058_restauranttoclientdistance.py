# Generated by Django 3.2 on 2021-07-27 22:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0057_auto_20210728_0141'),
    ]

    operations = [
        migrations.CreateModel(
            name='RestaurantToClientDistance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance', models.IntegerField(blank=True, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='restaurant_to_client_distance', to='foodcartapp.order')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='restaurant_to_client_distance', to='foodcartapp.restaurant')),
            ],
            options={
                'verbose_name': 'расстояние от ресторана до места',
                'verbose_name_plural': 'расстояния от ресторана до места',
            },
        ),
    ]
