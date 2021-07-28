from django.db import models


class Coordinates(models.Model):
    address = models.CharField(
        'название',
        max_length=64
    )
    lat = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    lng = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'координаты мест'
        verbose_name_plural = 'координаты мест'
