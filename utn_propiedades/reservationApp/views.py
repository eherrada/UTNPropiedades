import random
from datetime import datetime

from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout, authenticate
from django.contrib.auth import login as do_login
from django.db.models import Count, Q
from reservationApp.forms import CityForm
from django.contrib.auth.models import User
from reservationApp.models import Owner_Ship, City, Date_Rent, Reservation
from utn_propiedades.settings import ROOT_DIR


def welcome(request):
    order_type = ''
    filtro = Q(date_rent__reservation__isnull=True)

    if request.GET:
        order_type = request.GET['orderby']
    if request.method == 'POST':
        date1 = request.POST['fStart']
        date2 = request.POST['fEnd']
        qty = request.POST.get('qty', None)
        city =  request.POST.get('city')

        if qty != '':
            filtro =Q(capacity__gte=qty) & filtro

        if date1 != '' and date2 != '':
            filtro = filtro & Q(date_rent__date__range=[date1, date2])

        if city != '':
            cityA = City.objects.get(id=city)
            filtro = Q(city_id=cityA.id) & filtro



    propiedades_list = Owner_Ship.objects.filter(filtro).distinct()
    if order_type:
        if order_type == 'higher_price':
            propiedades_list = propiedades_list.order_by('-price')
        elif order_type == 'lower_price':
            propiedades_list = propiedades_list.order_by('price')
        elif order_type == 'higher_capacity':
            propiedades_list = propiedades_list.order_by('-capacity')
        else:
            propiedades_list = propiedades_list.order_by('capacity')

    if request.GET:
        order_type = request.GET['orderby']

    personas_por_propiedad = Owner_Ship.objects.values('capacity').annotate(capacity_count=Count('capacity')).order_by(
        '-capacity_count')

    ciudades_list = City.objects.all()
    propiedades_por_ciudad = Owner_Ship.objects.values('city').annotate(city_count=Count('city')).filter(
        date_rent__reservation__isnull=True).order_by('-city_count')

    return render(request, "reservationApp/welcome.html", {'propiedades_list': propiedades_list,
                                                            'ciudades_list': ciudades_list, 'root': ROOT_DIR,
                                                            'propiedades_por_ciudad': propiedades_por_ciudad,
                                                           'personas_por_propiedad' : personas_por_propiedad})

def detail(request, owner_ship_id):
        o = Owner_Ship.objects.get(id=owner_ship_id)
        h = o.owner
        dates = Date_Rent.objects.filter(owner_ship=o).filter(reservation=None)
        ciudades_list = City.objects.all()
        totalcapacity = o.capacity + 1
        capacity = range(1, totalcapacity)
        msg = ''
        if request.method == 'POST':
            date_list = request.POST.getlist('dates')
            my_reservation = Reservation(date=datetime.now(), code=random.randrange(999, 99999),
                                         total=int(o.price * len(date_list)), owner_ship=o, renter_name=request.POST['name'], renter_email=request.POST['email'], renter_phone=request.POST['phone'], host=h)
            my_reservation.save()
            new_date_list = []
            for date in date_list:
                date_new = Date_Rent.objects.filter(date=date).first()
                date_new.reservation = my_reservation
                date_new.save()
                new_date_list.append(date_new)
            return render(request, "reservationApp/reservationdetail.html",
                          {"reservation": my_reservation, "dates": new_date_list})

        return render(request, "reservationApp/detail.html",
                      {'ciudades_list': ciudades_list, 'owner_ship': o, 'capacity': capacity, 'dates': dates})


def reservation(request, reservation_id):
    my_reservation = Reservation.objects.filter(id=reservation_id).first()
    date_list = Date_Rent.objects.filter(reservation__id=reservation_id)

    return render(request, "reservationApp/reservationdetail.html", {"reservation": my_reservation, "dates": date_list})


def ownershipform(request):
    # Si estamos identificados devolvemos la portada
    ciudades_list = City.objects.all()
    error = ''
    msg = ''
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['desc']
        capacity = request.POST['capacity']
        price = request.POST['price']
        city = request.POST['city']
        my_city = ciudades_list.filter(name=city).first()
        image = request.FILES.get('file')
        if name is not None:
            p = Owner_Ship(name=name, description=description, price=price, capacity=capacity, city=my_city,
                           owner=request.user, image=image)
            p.save()
        else:
            error = 'Ups, algo ha ocurrido'
    if request.user.is_authenticated:
        return render(request, "reservationApp/ownershipform.html",
                      {'ciudades_list': ciudades_list, 'error': error, 'msg': msg})
    # En otro caso redireccionamos al login
    return redirect('/login')


def cityform(request):
    error = ''
    msg = ''
    form = CityForm()
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.save(commit=False)
            city.save()
            msg = 'Cargado Correctamente'
        else:
            error = 'La ciudad debe tener nombre'
    if request.user.is_authenticated:
        return render(request, "reservationApp/cityform.html", {'error': error, 'msg': msg, 'form': form})
        msg = ''
    return redirect('/login')


def login(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                do_login(request, user)
                print('entro')
                return redirect('/')

    return render(request, "reservationApp/login.html", {'form': form})


def userlist(request):
    userslist = User.objects.all()
    if request.user.is_authenticated:
        return render(request, "reservationApp/userlists.html", {'user_list': userslist})
    return redirect('/login')


def reservations(request):
    reservations = []
    if request.user.is_authenticated:
        if request.user.is_superuser:
            reservations = Reservation.objects.all()
        else:
            reservations = Reservation.objects.filter(host_id=request.user.id)


    return render(request, "reservationApp/reservations.html", {"reservations": reservations})

    return redirect('/login')


def logout(request):
    do_logout(request)
    return redirect('/')