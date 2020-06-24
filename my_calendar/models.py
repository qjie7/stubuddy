from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Event(models.Model):
    #event, Holiday, Exam
    # description
    # heading
    # datetime
    CHOICES = (
        ('EV', 'Event'),
        ('HD', 'Holiday'),
        ('EX', 'Exam')
    )
    type = models.CharField(blank=True, null=True,
                            choices=CHOICES, max_length=10, default='EV')
    title = models.CharField(max_length=100, default='Title')
    start = models.DateField()
    end = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.type + " =>  " + self.heading
