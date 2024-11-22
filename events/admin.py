from django.contrib import admin

from .models import Hall
from .models import Booking
from .models import Appointment
from .models import CustomUser
admin.site.register(Hall)
admin.site.register(Booking)
admin.site.register(CustomUser)

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'date', 'time', 'purpose')
    search_fields = ('name', 'email', 'phone', 'purpose')
    list_filter = ('date',)

admin.site.register(Appointment, AppointmentAdmin)
