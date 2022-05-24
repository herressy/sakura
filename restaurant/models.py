from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import datetime
from django.db.models import Q


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(delete=False)


class SoftDeleteModel(models.Model):
    objects = SoftDeleteManager()
    all_objects = models.Manager()
    delete = models.BooleanField(default=False)

    class Meta:
        abstract = True


class NameField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(NameField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()


class User(AbstractUser):
    username = NameField(
        max_length=50, 
        unique=True, 
        help_text='Use the following format: firstname_surname'
    )
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=14, blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        positions = self.groups.values_list('name', flat=True)
        return f"{self.username} {list(positions)}"


class Table(SoftDeleteModel):
    server = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        related_name='tables', 
        null=True,
        limit_choices_to=(
            Q(groups__name='Servers') | 
            Q(is_superuser=True)
        )
    )
    cook = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        related_name='table', 
        null=True,
        limit_choices_to=(
            Q(groups__name='Cooks') | 
            Q(is_superuser=True)
        )
    )
    number = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 20)], 
        unique=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def is_closed(self):
        now = timezone.now()
        if self.created_at + datetime.timedelta(minutes=20) < now:
            return '(closed)'
        return ''

    @property
    def guest_count(self):
        # There may be more orders per seat; 
        # distinct for seat is needed before counting.
        return self.order_set.values('seat').distinct().count()

    def __str__(self) -> str:
        return f'Table {self.number}'


class Meal(models.Model):
    kind = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()

    class Meta:
        ordering = ['kind']

    def __str__(self) -> str:
        return f'{self.kind}: {self.name}'


class Order(SoftDeleteModel):
    seat = models.IntegerField(
        choices=[(i, i) for i in range(1, 11)]
    )
    table = models.ForeignKey(
        Table, 
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    STEAK_CHOICES = (
        ('rare', 'rare'),
        ('medium rare', 'medium rare'),
        ('medium', 'medium'),
        ('medium well', 'medium well'),
        ('well done', 'well done'),
    )
    meal = models.ManyToManyField(Meal, blank=True)
    steak = models.CharField(
        max_length=50, 
        choices=STEAK_CHOICES, 
        blank=True, 
        null=True
    )
    notes = models.CharField(
        max_length=200, 
        blank=True, 
        null=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'table {self.table}: seat {self.seat}'
