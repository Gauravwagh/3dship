from django.db import models

# Create your models here.

class PositionConstants(models.Model):
    x_constant = models.IntegerField(null=True, blank=True)
    y_constant = models.IntegerField(null=True, blank=True)
    z_constant = models.IntegerField(null=True, blank=True)

class Ports(models.Model):
    port_number = models.IntegerField(null=True, blank=True)
    number_of_containers = models.IntegerField(null=True, blank=True)


class ContainerPosition(models.Model):
    port = models.ForeignKey(Ports, null=True, blank=True)
    x_position = models.IntegerField(null=True, blank=True, verbose_name="row")
    y_position = models.IntegerField(null=True, blank=True, verbose_name="column")
    z_position = models.IntegerField(null=True, blank=True, verbose_name="height")


