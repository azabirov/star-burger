# Generated by Django 3.2 on 2021-07-27 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0045_ordereditem_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('processed', 'Обработанный'), ('unprocessed', 'Необработанный')], db_index=True, default='unprocessed', max_length=64),
        ),
    ]
