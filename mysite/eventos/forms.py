from datetime import timedelta, datetime
from tinymce.widgets import TinyMCE
from .services import DataService
from django import forms
from django.utils.safestring import mark_safe
from .models import EventEco


class ImageWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        if value:
            return mark_safe(f'<img src="{value}" style="max-width: 100px; max-height: 100px;" />')
        return ''


class CreateEventEcoFormAdmin(forms.ModelForm):

    class Meta:
        model = EventEco
        fields = ('id',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = DataService()
        self.preset_events = self.service.get_sympla_events_not_in_database()

        blank_event = EventEco(
            id=len(self.service.get_database_events()),
            start_date=datetime.now(),
            end_date=datetime.now(),
            name="Novo Evento em Branco",
            detail="Insira aqui a descrição do novo evento",
            private_event=False,
            published=False,
            cancelled=False,
            image="https://sua-imagem-aqui.com.br",
            url="https://sua-url-aqui.com.br",
        )

        self.preset_events.append(blank_event)

        self.fields['id'] = forms.ChoiceField(
            choices=[(event.id, event.start_date.strftime('%d/%m/%Y')+' - '+event.name) for event in self.preset_events]
        )

        self.fields['id'].label = 'Predefinição'
        self.fields['id'].help_text = 'Os eventos criados em branco não serão criados no Sympla'

    # many-to-many desabilitado
    def save_m2m(self):
        pass

    def save(self, commit=True):
        if 'id' in self.cleaned_data:
            preset_id = self.cleaned_data['id']

            preset = None
            for event in self.preset_events:
                if int(event.id) == int(preset_id):
                    preset = event

            # print(id)
            event_eco = EventEco.objects.create(
                id=preset.id,
                start_date=preset.start_date,
                end_date=preset.end_date,
                name=preset.name,
                detail=preset.detail,
                private_event=preset.private_event,
                published=preset.published,
                cancelled=preset.cancelled,
                image=preset.image,
                url=preset.url
            )
            return event_eco
        else:
            return super().save(commit=commit)


class EditEventEcoFormAdmin(forms.ModelForm):
    image_preview = forms.ImageField(widget=ImageWidget, required=False)

    class Meta:
        model = EventEco
        fields = (
            'id',
            'name',
            'start_date',
            'end_date',
            'published',
            'detail',
            'url',
            'image',
        )
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),  # Widget para selecionar data e horário
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),  # Widget para selecionar data e horário
            "detail": TinyMCE(),  # Defina o tamanho máximo desejado aqui
            'name': forms.TextInput(attrs={'size': 50}),
            'url': forms.TextInput(attrs={'size': 90}),
            'image': forms.TextInput(attrs={'size': 90}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['start_date'] = (self.instance.start_date - timedelta(hours=3)).strftime('%Y-%m-%dT%H:%M')
        self.initial['end_date'] = (self.instance.end_date - timedelta(hours=3)).strftime('%Y-%m-%dT%H:%M')
        self.fields['image_preview'].initial = self.instance.image

        instance = kwargs.get('instance')
        self.service = DataService()

        if instance:
            if instance.id > 2300000:

                self.fields['id'].widget.attrs['readonly'] = True
            else:
                preset_events = self.service.get_sympla_events_not_in_database()

                choices = [(event.id, event.start_date.strftime('%d/%m/%Y')+' - '+event.name) for event in preset_events]
                choices.insert(0, (instance.id, '----------'))
                self.fields['id'].widget = forms.Select(choices=choices)

    def as_p(self):
        return super().as_p() + self.image_preview.tag()  # Adiciona a tag da imagem após o formulário renderizado


class EditDetailEventEcoForm(forms.ModelForm):
    class Meta:
        model = EventEco
        fields = (
            'detail',
        )
        widgets = {
            "detail": TinyMCE(),  # Defina o tamanho máximo desejado aqui
        }
