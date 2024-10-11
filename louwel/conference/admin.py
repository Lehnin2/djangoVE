from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from .models import Conference
from user.models import *
from django.db.models import Count

class ReservationInline(admin.TabularInline):
    model=reservation
    extra=1
    can_delete=True
    readonly_fields=('reservation_date',)
class ParticipantFilter(admin.SimpleListFilter):
    title="participant_filter"
    parameter_name="participant"
    def lookups(self,request,admin_model) :
        return (
            ('0',('no participant')),
            ('more',('moare participants'))
        )
    def queryset(self, request, queryset) :
        if self.value()=='0':
            return queryset.annotate(participant_count=Count('reservations')).filter(participant_count=0)
        if self.value()=='more':
            return queryset.annotate(participant_count=Count('reservation')).filter(participant_count__gt=0)   
        return queryset
class conferenceDateFilter(admin.SimpleListFilter):
    title='date conf filter'
    parameter_name="conference_date"
    def lookups(self, request, model_admin) :
        return (
            ('past','past conf'),
            ('today','today conf'),
            ('upcomming','upcomming conf'),
        )
    def queryset(self,request,queryset):
        if self.value()=='past':
            return queryset.filter(end_date__lt=timezone.now().date())
        if self.value()=='today':
            return queryset.filter(end_date=timezone.now().date())
        if self.value()=='upcomming':
            return queryset.filter(end_date__gt=timezone.now().date())
class ConferenceAdmin(admin.ModelAdmin):
    inlines = [ReservationInline]
    list_display = ('title','location', 'start_date', 'end_date',  'price')
    search_fields = ('title',)
    list_per_page= 5
    ordering= ('start_date',)
    
    fieldsets = (
         ('Description', {
            'fields': ('title', 'description')
        }),
        ('Horaires de la conférence', {
            'fields': ('start_date', 'end_date')
        }),
        ('Informations pratiques', {
            'fields': ('location', 'price', 'capacity')
        }),
        ('Documents', {
            'fields': ('program',)
        }),
        ('Catégorie de participant', {
            'fields': ('category',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Optional: Makes this section collapsible
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at') 
    autocomplete_fields=("category",)
    list_filter=('title',ParticipantFilter,conferenceDateFilter)
# Register your models here.
admin.site.register(Conference, ConferenceAdmin)