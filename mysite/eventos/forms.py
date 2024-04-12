from datetime import timedelta
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
        fields = ('preset',)

    def __init__(self, *args, **kwargs):
        self.service = DataService()
        super().__init__(*args, **kwargs)
        events = self.service.get_events()
        self.sympla_events = [event for event in events if event.event_eco is None]

        self.fields['preset'] = forms.ChoiceField(
            choices=[(event.event_id, event.start_date.strftime('%d/%m/%Y')+' - '+event.name) for event in self.sympla_events]
        )

    def save_m2m(self):
        pass  # Você pode adicionar lógica aqui se necessário

    def save(self, commit=True):
        if 'preset' in self.cleaned_data:
            preset_id = self.cleaned_data['preset']
            print('preset_id', preset_id)

            preset = None
            for event in self.sympla_events:
                if int(event.event_id) == int(preset_id):
                    preset = event

            event_eco = EventEco.objects.create(
                event_id=preset.event_id,
                start_date=preset.start_date,
                end_date=preset.end_date,
                name=preset.name,
                detail=preset.detail,
                private_event=preset.private_event,
                published=preset.published,
                cancelled=preset.cancelled,
                image=preset.image,
                url=preset.url,
                preset=preset_id
            )
            return event_eco
        else:
            return super().save(commit=commit)


class EditEventEcoFormAdmin(forms.ModelForm):
    image_preview = forms.ImageField(widget=ImageWidget, required=False)

    class Meta:
        model = EventEco
        fields = (
            'event_id',
            'name',
            'start_date',
            'end_date',
            'published',
            'detail',
            'url',
            'image',
        )
        widgets = {
            'event_id': forms.TextInput(attrs={'readonly': 'readonly'}),  # Campo event_id bloqueado para edição
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
