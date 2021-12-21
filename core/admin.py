from django.contrib import admin
from core.models import Eventos


class EventosAdmin(admin.ModelAdmin):
  list_display = ('id', 'title', 'event_date', 'creation_date')
  list_filter = ('title', 'event_date', 'user',)

admin.site.register(Eventos, EventosAdmin)
