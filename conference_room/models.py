from django.db import models


class Room(models.Model):
    room_name = models.CharField(max_length=255, unique=True)
    capacity = models.SmallIntegerField()
    projector_availability = models.BooleanField(default=False)


class Reservation(models.Model):
    date = models.DateField()
    room = models.CharField(max_length=64)
    comment = models.CharField(max_length=255, default="No comment")

    class Meta:
        unique_together = ('date', 'room',)
