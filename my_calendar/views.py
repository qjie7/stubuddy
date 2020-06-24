from django.shortcuts import render, redirect
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from .forms import EventForm
from .models import Event
from django.contrib.auth.decorators import login_required

import json

# Create your views here.


@login_required
def add_event(request):
    if request.POST:
        form = EventForm(request.POST)
        if form.is_valid():
            new_event = form.save(commit=False)
            new_event.owner = request.user
            new_event.save()
            return redirect('my_calendar:view')
            # return render(request, 'my_calendar/success.html')

        return render(request, 'my_calendar/index.html', context={'form': form})
    return render(request, 'my_calendar/index.html', context={'form': EventForm()})


@login_required
def calendar(request):
    events = eval(serializers.serialize("json", Event.objects.filter(owner=request.user)))
    # print(events[0])
    events = list(map(lambda x: x['fields'], events))
    print(events)
    return render(request, 'my_calendar/calendar.html', context={'events': events})


def success(request):
    return render(request, 'my_calendar/success.html')
