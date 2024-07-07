from django.shortcuts import render
from .services import DataService
from .utils import *

from django.urls import reverse
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from .models import EventEco

class EventEcoDetail(DetailView):
    context_object_name = 'eventeco'
    template_name = "eventeco_detail.html"

    def get_object(self, queryset=None):
        dataservice = DataService()
        event = dataservice.get_valid_event_by_id(self.kwargs.get('pk'))
        return event

def search_event(request):
    dataservice = DataService()
    events = []
    count = 0
    search = ''

    if request.method == 'POST':
        search = request.POST.get('search')
        events = dataservice.get_events_by_filter(search)
        count = events.__len__()

    return render(request, 'search.html', { 'events': events, 'count': count, 'search': search })

def enviar_email_evento(request):
    dataservice = DataService()
    categories = dataservice.get_events_categories()  # Get all primary categories

    participants = []
    selected_category = request.GET.get('category')
    action = request.GET.get('action')
    
    if selected_category:
        # Filtre os participantes com base na categoria selecionada
        participants = dataservice.get_sympla_participant_by_category(selected_category)

    if action == 'send_email' and participants:
        # Enviar email para os participantes filtrados
        to_emails = [participant.email for participant in participants]
        subject = "EventEco"
        content = "Conteúdo do email."
        # print(send_mailer_send_email(to_emails, subject, content))
        send_test_email(to_emails,subject,content)
    return render(request, 'email.html', {'categories': categories, 'selected_category': selected_category,'participants': participants})
    
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