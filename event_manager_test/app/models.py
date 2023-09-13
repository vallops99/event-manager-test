"""DB models."""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Event(models.Model):
    """Event DB model."""
    class Type(models.TextChoices):
        """Event's type."""
        HIKE = 'hike', 'Hike'
        DISCO = 'disco', 'Disco'
        TRAVEL = 'travel', 'Travel'
        MEETUP = 'meetup', 'Meet Up'

    class Status(models.IntegerChoices):
        """Event's status."""
        ENDED = 50, 'ENDED'
        ENDING = 40, 'ENDING'
        JOINING = 30, 'JOINING'
        STARTED = 20, 'STARTED'
        CONFIRMED = 10, 'CONFIRMED'

    name = models.CharField(max_length=100)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    e_type = models.CharField(
        choices=Type.choices,
        default=Type.MEETUP,
        max_length=6
    )
    status = models.PositiveSmallIntegerField(
        choices=Status.choices,
        default=Status.CONFIRMED
    )
    capacity = models.IntegerField(
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owner'
    )
    registered_users = models.ManyToManyField(
        User,
        blank=True,
        related_name='events'
    )

    def __str__(self):
        return self.name

    @property
    def partecipants_quantity(self):
        """Get quantity of registered users."""
        return self.registered_users.count()
