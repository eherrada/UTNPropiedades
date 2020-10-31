from django.contrib import admin
# Register your models here.
from reservationApp.models import Date_Rent, City, Reservation, Owner_Ship

class Date_Rent_Inline(admin.TabularInline):
    model = Date_Rent
    fk_name = "owner_ship"
    max_num = 7


class OwnerShipAdmin(admin.ModelAdmin):
    inlines = [Date_Rent_Inline, ]
    list_display = ("name", "city", "capacity", "price", "owner")
    search_fields = ("name", "capacity", "price",)

class CitiesAdmin(admin.ModelAdmin):
    list_display = ("name", "province")
    search_fields = ("name", "province",)
    list_filter = ("province", )


class Date_RentAdmin(admin.ModelAdmin):
    list_display = ("date", "owner_ship", "reservation")
    search_fields = ("date",)
    list_filter = ("date",)

class ReservationAdmin(admin.ModelAdmin):
    list_display = ("date", "host", "owner_ship", "renter_name", "total")
    search_fields = ("date", "renter_name", "total",)
    list_filter = ("date",)



admin.site.register(City, CitiesAdmin)
admin.site.register(Date_Rent, Date_RentAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Owner_Ship, OwnerShipAdmin)








