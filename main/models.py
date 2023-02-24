from django.db import models
from users.models import Customer


class Event(models.Model):
    title = models.CharField(max_length=150)
    thumbnail = models.ImageField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class EventUsers(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True, null=True, blank=True)

