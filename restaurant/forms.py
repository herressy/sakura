from django.forms import ModelForm
from .models import *

class TableForm(ModelForm):
    class Meta:
        model = Table
        fields = '__all__'

class OrderForm(ModelForm):
    class Meta:
        model = Order
        exclude = ['table']