# Generated by Django 3.2 on 2021-07-27 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0047_auto_20210727_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='comment',
            field=models.TextField(blank=True, max_length=256, verbose_name='комментарий'),
        ),
    ]
