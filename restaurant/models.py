from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Q
from django.db.models.signals import post_save, pre_save
from django.core.mail import send_mail
from django.core.validators import RegexValidator

from datetime import timedelta


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class SoftDeleteModel(models.Model):
    objects = SoftDeleteManager()
    all_objects = models.Manager()
    deleted = models.BooleanField(default=False, editable=False)

    def soft_delete(self):
        self.deleted = True
        self.save()

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
        help_text='Use the following format: firstname_lastname',
        validators=[RegexValidator(
            regex='^[a-zA-Z]+_[a-zA-Z]+$',
            message='Use the following format: firstname_lastname',
            code='invalid_username'
            ),
        ]
    )
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=14, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        position = self.groups.values_list('name',flat = True)
        return f"{self.username} {list(position)}"


class Table(SoftDeleteModel):
    server = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        related_name='tables', 
        null=True,
        limit_choices_to=(
            Q(groups__name='servers') | 
            Q(is_superuser=True)
        )
    )
    cook = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        related_name='table', 
        null=True,
        limit_choices_to=(
            Q(groups__name='cooks') | 
            Q(is_superuser=True)
        )
    )
    number = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 20)], 
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def is_closed(self):
        now = timezone.now()
        if self.created_at + timedelta(minutes=20) < now:
            return ' (closed)'
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
    meal = models.ManyToManyField(Meal, blank=True)
    STEAK_CHOICES = (
        ('rare', 'rare'),
        ('medium rare', 'medium rare'),
        ('medium', 'medium'),
        ('medium well', 'medium well'),
        ('well done', 'well done'),
    )
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


@receiver(post_save, sender=Table)
def notify_cook(sender, instance, **kwargs):
    if not instance.deleted:
        send_mail(
            'You have a new table!',
            f'You have been assigned to {instance}. \
            Check the table for order updates.',
            'admin@sakura.com',
            [f'{instance.cook.email}'],
            fail_silently=False
        )

@receiver(pre_save, sender=Group)
def verify_group_name(sender, instance, **kwargs):
    valid_group_names = ['server', 'hostess', 'cook', 'manager']
    if not instance.name in valid_group_names:
        raise Exception('Invalid group name!')