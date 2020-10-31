from django import forms

from .models import City, Owner_Ship


class CityForm(forms.ModelForm):
    name = forms.CharField(label='Nombre:', max_length=15)
    province = forms.CharField(label='Provincia', max_length=20)

    class Meta:
        model = City
        fields = ('name', 'province',)

class OwnerShipForm(forms.Form):
    ciudades_list = City.objects.all()
    name = forms.CharField(label='Nombre:', max_length=15)
    description = forms.Textarea()
    capacity = forms.IntegerField(label='Capacidad:')
    price = forms.IntegerField(label='Precio:')
    city = forms.ChoiceField(choices=ciudades_list)
    image = forms.ImageField(label='Imagen')

    class meta:
        model = Owner_Ship
        fields = ('name', 'description', 'capacity', 'price', 'city', 'image',)