from django.contrib import admin
from .models import Participant,reservation
# Register your models here.
admin.site.register(Participant)
@admin.register(reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('conference', 'participant', 'confirmed', 'reservation_date')
    search_fields = ('participant__username', 'conference__title') 