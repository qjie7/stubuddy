from django.forms import ModelForm, DateInput
from .models import Event


class DateInput(DateInput):
    input_type = 'date'


class EventForm(ModelForm):
    class Meta:
        model = Event
        #fields = '__all__'
        fields = ['type', 'title', 'start', 'end']
        widgets = {
            'start': DateInput(),
            'end': DateInput(),
        }
