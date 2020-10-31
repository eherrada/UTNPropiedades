# Generated by Django 2.2.7 on 2020-10-25 12:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nombre')),
                ('province', models.CharField(max_length=50, verbose_name='Provincia')),
            ],
            options={
                'verbose_name_plural': 'Ciudades',
            },
        ),
        migrations.CreateModel(
            name='Owner_Ship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nombre')),
                ('description', models.CharField(max_length=200, verbose_name='Descripción')),
                ('price', models.IntegerField(verbose_name='Precio')),
                ('capacity', models.IntegerField(verbose_name='Capacidad')),
                ('image', models.ImageField(null=True, upload_to='application/img', verbose_name='Imagen')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reservationApp.City', verbose_name='Ciudad')),
                ('owner', models.ForeignKey(on_delete=models.SET('null'), to=settings.AUTH_USER_MODEL, verbose_name='Dueño')),
            ],
            options={
                'verbose_name_plural': 'Propiedades',
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Fecha')),
                ('code', models.IntegerField(verbose_name='Código')),
                ('total', models.IntegerField(verbose_name='Total')),
                ('renter_name', models.CharField(default='no_name', max_length=80, verbose_name='Nombre del Huesped')),
                ('renter_email', models.CharField(default='@', max_length=100, verbose_name='Email del Huesped')),
                ('renter_phone', models.CharField(default='no_phone', max_length=25, verbose_name='Teléfono del Huesped')),
                ('host', models.ForeignKey(on_delete=models.SET('null'), to=settings.AUTH_USER_MODEL, verbose_name='Propietario')),
                ('owner_ship', models.ForeignKey(on_delete=models.SET('null'), to='reservationApp.Owner_Ship', verbose_name='Propiedad')),
            ],
            options={
                'verbose_name_plural': 'Reservas',
            },
        ),
        migrations.CreateModel(
            name='Date_Rent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Fecha de alquiler')),
                ('owner_ship', models.ForeignKey(on_delete=models.SET('null'), to='reservationApp.Owner_Ship', verbose_name='Propiedad')),
                ('reservation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='reservationApp.Reservation', verbose_name='Reserva')),
            ],
            options={
                'verbose_name_plural': 'Fechas de Alquileres',
            },
        ),
    ]
