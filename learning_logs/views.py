from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.


def index(request):
    """ The Home page for Learning Log """
    return render(request, 'learning_logs/index.html')

# login_required - checks whether a user is logged in, and then runs the code in topics() only if logged in
# if not logged in, then redirect to the login page.
@login_required
def topics(request):
    """ Show topics to specific logged in user  """
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')

    # topics = Topic.objects.order_by('date_added') --  show all topics
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """ Show a single topic and all its entries """
    topic = Topic.objects.get(id=topic_id)

    # Make sure the topic belongs to the current_user
    check_topic_owner(request, topic)

    # minus sign before date_added indicates reverse order
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """ Add a new topic """
    if request.method != "POST":
        # No data submitted; Create a blank form
        form = TopicForm()
    else:
        # POST data submitted; process data

        # request.POST - data input from the user
        form = TopicForm(data=request.POST)

        # is_valid() - auto checks that all required fields have been filled in and correctly (based on models.py)
        if form.is_valid():
            new_topic = form.save(commit=False)
            
            # specify which topic belong to which user
            new_topic.owner = request.user
            new_topic.save()
            # form.save()

            # Once data is saved, we can leave this page
            return redirect('learning_logs:topics')

    # Display a blank or invalid form
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """ Add a new entry for a particular topic """
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(request, topic)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data
        form = EntryForm(data=request.POST)
        if form.is_valid():
            # commmit=False -> tell Django to create a new entry object and assign it to new_entry without saving it to the database yet.
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    # Display a blank or invalid form
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """ Edit an existing entry """
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    # Make sure the topic belongs to the current_user
    check_topic_owner(request, topic)

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data
        # Create a form instance based on the information associated with the existing entry object
        # updated with any relevant data from request.POST
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


def check_topic_owner(request, topic):
    """ Check whether the topic is  belong to the current logged in user"""
    if topic.owner != request.user:
        # 404 error - request resource doesn't exist on a server
        raise Http404 