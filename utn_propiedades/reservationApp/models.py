from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models


class City(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nombre")
    province = models.CharField(max_length=50, verbose_name="Provincia")

    class Meta:
        verbose_name_plural = 'Ciudades'

    def __str__(self):
        return self.name


class Owner_Ship(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nombre")
    description = models.CharField(max_length=200, verbose_name="Descripción")
    price = models.IntegerField(verbose_name="Precio")
    capacity = models.IntegerField(verbose_name="Capacidad")
    city = models.ForeignKey(City, null=True, on_delete=models.SET_NULL, verbose_name="Ciudad")
    owner = models.ForeignKey(User, null=False, on_delete=models.SET('null'), verbose_name="Dueño")
    image = models.ImageField(upload_to='application/img', null=True, verbose_name="Imagen")

    class Meta:
        verbose_name_plural = 'Propiedades'

    def __str__(self):
        return self.name


class Reservation(models.Model):
    date = models.DateField(verbose_name="Fecha")
    code = models.IntegerField(verbose_name="Código")
    total = models.IntegerField(verbose_name="Total")
    owner_ship = models.ForeignKey(Owner_Ship, null=False, on_delete=models.SET('null'), verbose_name="Propiedad")
    renter_name = models.CharField(max_length=80, default="no_name", verbose_name="Nombre del Huesped")
    renter_email = models.CharField(max_length=100, default="@", verbose_name="Email del Huesped")
    renter_phone = models.CharField(max_length=25, default="no_phone", verbose_name="Teléfono del Huesped")
    host = models.ForeignKey(User, null=False, on_delete=models.SET('null'), verbose_name="Propietario")

    class Meta:
        verbose_name_plural = 'Reservas'

    def __str__(self):
        return str(self.code)


class Date_Rent(models.Model):
    date = models.DateField(verbose_name="Fecha de alquiler")
    owner_ship = models.ForeignKey(Owner_Ship, null=False, on_delete=models.SET('null'), verbose_name="Propiedad")
    reservation = models.ForeignKey(Reservation, null=True, on_delete=models.SET_NULL, blank=True,
                                    verbose_name="Reserva")

    class Meta:
        verbose_name_plural = 'Fechas de Alquileres'

    def __str__(self):
        return self.date.__format__("%Y-%m-%d")
