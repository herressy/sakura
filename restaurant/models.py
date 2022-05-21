from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import datetime

from .menu import *

class NameField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(NameField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()

class User(AbstractUser):
  username = NameField(max_length=50, unique=True, help_text='Use the following format: firstname_surname')
  email = models.EmailField(unique=True)
  phone_number = models.CharField(max_length=14, blank=True)
  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['email']

  def __str__(self):
      positions = self.groups.values_list('name', flat=True)
      return f"{self.username} {list(positions)}"

class Table(models.Model):
    server = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='tables', null=True)
    cook = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='table', null=True)
    number = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 20)], unique=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def is_closed(self):
        now = timezone.now()
        if self.created_at + datetime.timedelta(minutes=20) < now:
            return True

    @property
    def guest_count(self):
        return self.order_set.values('seat').distinct().count()

    def __str__(self) -> str:
        return f'Table {self.number}'

class Meal(models.Model):
    KIND_CHOICES = (
        ('appetizer', 'appetizer'),
        ('entree', 'entree'),
        ('side', 'side'),
        ('other', 'other'),
        ('rice', 'rice'),
    )
    kind = models.CharField(max_length=50, choices=KIND_CHOICES)
    name = models.CharField(max_length=100, blank=True, null=True)
    price = models.PositiveIntegerField()

    class Meta:
        ordering = ['kind']

    def __str__(self) -> str:
        return f'{self.kind}: {self.name}'

class Order(models.Model):
    seat = models.IntegerField(choices=[(i, i) for i in range(1, 11)])
    table = models.ForeignKey(Table, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    STEAK_CHOICES = (
        ('rare', 'rare'),
        ('medium rare', 'medium rare'),
        ('medium', 'medium'),
        ('medium well', 'medium well'),
        ('well done', 'well done'),
    )
    notes = models.CharField(max_length=200, blank=True, null=True)
    meal = models.ManyToManyField(Meal, blank=True)
    steak = models.CharField(max_length=50, choices=STEAK_CHOICES, blank=True, null=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self) -> str:
        return f'table {self.table}: seat {self.seat}'