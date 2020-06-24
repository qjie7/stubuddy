from django import forms
from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    class Meta:

        # build a from from the Topic model 
        model = Topic

        # include only the text field
        fields = ['text']

        # tells Django not to generate a label for the text field
        labels = {'text': ''}
    
class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': 'Entry:'}

        # widgets is an HTML form element, such as a single line text box, multiline text area or
        # or drop-down list.
        widgets = {'text': forms.Textarea(attrs={'cols':80})}