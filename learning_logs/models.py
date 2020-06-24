from django.db import models
from django.contrib.auth.models import User

# Inherits from Model - a parent class included in Django that defines a model's basic functionality
class Topic(models.Model):
    """ a topic the user is learning about  """
    text = models.CharField(max_length=200)

    # auto_now_add=True --> tells Django to automatically set this attribute to the current date and time whenever the user creates a new topic
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """ Return a string representation of the model """
        return self.text


class Entry(models.Model):
    """ Something specific learned about a topic """

    # on_delete=models.CASCADE --> tell Django that when a topic is deleted, all the entries associated with that topic should be deleted as well
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        """ Tell Django to use 'Entries' when it needs to refer to more than one entry (Plural)
            Without this, Django would refer to multiple entries as 'Entrys'
            By default, Django adds a 's' to a table name in the admin page. """

        verbose_name_plural = 'entries'

    def __str__(self):
        """ Return a string representation of the model """
        # Show just first 50 characters of text in the admin page(easy references)
        # ... to clarify that we're not always displaying the entire entry
        if len(self.text) < 50:
            return self.text
        else:
            return f"{self.text[:50]}..."
