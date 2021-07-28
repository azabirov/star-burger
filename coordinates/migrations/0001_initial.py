# Generated by Django 3.2 on 2021-07-28 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coordinates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=64, verbose_name='название')),
                ('lat', models.DecimalField(blank=True, decimal_places=8, max_digits=11, null=True)),
                ('lng', models.DecimalField(blank=True, decimal_places=8, max_digits=11, null=True)),
            ],
            options={
                'verbose_name': 'координаты мест',
                'verbose_name_plural': 'координаты мест',
            },
        ),
    ]
