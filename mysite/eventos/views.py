from django.http import HttpResponse
from .services import DataService

from django.urls import reverse
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import EditDetailEventEcoForm
from .models import EventEco
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator


@method_decorator(staff_member_required, name='dispatch')
class UpdateEventEcoDetail(SuccessMessageMixin, UpdateView):
    form_class = EditDetailEventEcoForm
    model = EventEco
    context_object_name = 'eventeco'
    template_name = "edit_eventeco.html"
    success_message = "Edited Succesfully"

    def get_success_url(self):
        return reverse('eventeco_detail', kwargs={'pk': self.object.pk})


class EventEcoDetail(DetailView):
    context_object_name = 'eventeco'
    template_name = "eventeco_detail.html"

    def get_object(self, queryset=None):
        dataservice = DataService()
        event = dataservice.get_valid_event_by_id(self.kwargs.get('pk'))
        return event


def index(request):
    service = DataService()
    html = "Hello, world. You're at the eventos index.<br>"
    for evento in service.get_valid_events():
        html += '<b>EVENT_ID:</b> ' + str(evento.id) + '<br>'
        html += '<b>NAME:</b> ' + evento.name + '<br>'

        if isinstance(evento, EventEco):
            html += '<b>CRIADO NA BASE:</b> ✅ <br>'

        else:
            html += '<b>CRIADO NA BASE:</b> ❌ <br>'

        html += f"<a href=\"http://127.0.0.1:8000/eventos/{evento.id}\"><button>Ver Evento</button></a><br>"
        html += "<br>"

    return HttpResponse(html)
