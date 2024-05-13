from django.http import HttpResponse
from django.shortcuts import render
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

def enviar_email_evento(request):
    dataservice = DataService()
    categories = dataservice.get_events_categories()  # Get all primary categories

    participants = None
    
    if request.method == 'POST':
        category = request.POST.get('category')

        if category:
            participants = dataservice.get_sympla_participant_by_category(category)
        else:
            participants = None

        # Here you would add logic to send email to participants, for example, using Django's Email package

    return render(request, 'email.html', {'categories': categories, 'participants': participants})

def index(request):
    service = DataService()
    events = service.get_valid_events()
    eventos_dict = [evento_to_dict(event) for event in events]
    return render(request, 'index.html', { 'events': eventos_dict })

def evento_to_dict(event):
    return {
        "id": event.id,
        "name": event.name,
        "is_eco": isinstance(event, EventEco),
        "start_date": event.start_date,
        "end_date": event.end_date
    }