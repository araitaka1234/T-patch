from django.contrib import admin

# Register your models here.
from .models import Item
from .models import Schedule

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):

    class Meta:
        verbose_name = 'ユーザ'
        verbose_name_plural = 'ユーザ'

admin.site.register(Schedule)
