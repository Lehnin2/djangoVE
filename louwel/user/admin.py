# admin.py

from django.contrib import admin
from .models import Participant, reservation
from django.db.models import Count
from django.utils import timezone

class ReservationInline(admin.TabularInline):
    model = reservation
    extra = 1
    can_delete = True
    readonly_fields = ('reservation_date',)

class ParticipantReservationFilter(admin.SimpleListFilter):
    title = "reservation filter"
    parameter_name = "reservations"

    def lookups(self, request, model_admin):
        return (
            ('0', 'No reservations'),
            ('more', 'Has reservations')
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.annotate(reservation_count=Count('reservations')).filter(reservation_count=0)
        if self.value() == 'more':
            return queryset.annotate(reservation_count=Count('reservations')).filter(reservation_count__gt=0)
        return queryset

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'participant_category', 'created_at')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    list_per_page = 2
    ordering = ('username',) #ordre inverse('_start_date')
    list_filter = ('participant_category', ParticipantReservationFilter)
    inlines = [ReservationInline]

    fieldsets = (
        ('Personal Info', {
            'fields': ('username', 'first_name', 'last_name', 'email', 'cin')
        }),
        ('Category', {
            'fields': ('participant_category',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'update_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'update_at')

class ReservationDateFilter(admin.SimpleListFilter):
    title = 'Reservation Date Filter'
    parameter_name = 'reservation_date'

    def lookups(self, request, model_admin):
        return (
            ('past', 'Past reservations'),
            ('today', 'Today\'s reservations'),
            ('upcoming', 'Upcoming reservations'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'past':
            return queryset.filter(conference__end_date__lt=timezone.now().date())
        if self.value() == 'today':
            return queryset.filter(conference__start_date__lte=timezone.now().date(), conference__end_date__gte=timezone.now().date())
        if self.value() == 'upcoming':
            return queryset.filter(conference__start_date__gt=timezone.now().date())
        return queryset
def mark_as_confirmed(modeladmin, request, queryset):
    queryset.update(confirmed=True)
mark_as_confirmed.short_description = "Marquer les réservations sélectionnées comme confirmées"

def mark_as_unconfirmed(modeladmin, request, queryset):
    queryset.update(confirmed=False)
mark_as_unconfirmed.short_description = "Marquer les réservations sélectionnées comme non confirmées"
@admin.register(reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('conference', 'participant', 'confirmed', 'reservation_date')
    search_fields = ('participant__username', 'conference__title')
    list_per_page = 10
    list_filter = ('confirmed', ReservationDateFilter,'participant')
    ordering = ('reservation_date',)
    actions = [mark_as_confirmed, mark_as_unconfirmed]
