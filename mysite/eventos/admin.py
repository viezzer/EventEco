from .models import EventEco
from django.contrib import admin
from .forms import CreateEventEcoFormAdmin, EditEventEcoFormAdmin


class EventEcoAdmin(admin.ModelAdmin):
    form = CreateEventEcoFormAdmin
    list_display = ['event_id', 'name', 'start_date', 'published',]
    sortable_by = ['name']
    ordering = ['-start_date', 'name']

    def get_form(self, request, obj=None, **kwargs):
        if obj:  # Se estiver editando um objeto existente
            return EditEventEcoFormAdmin
        else:  # Se estiver criando um novo objeto
            return CreateEventEcoFormAdmin


admin.site.register(EventEco, EventEcoAdmin)
