from django.contrib import admin
from .models import category
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields=('title',)
admin.site.register(category,CategoryAdmin)