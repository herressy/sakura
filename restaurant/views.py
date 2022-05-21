from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.views.generic.edit import CreateView
from .models import *
from .forms import TableForm, OrderForm
from django.views.generic.detail import DetailView
from django.forms.models import model_to_dict
import datetime
from django.contrib import messages

def home(request):
    tables = Table.objects.all()
    context = {'tables': tables}
    return render(request, 'restaurant/home.html', context)

def create_table(request):
    form = TableForm()

    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('home')

    context = {'form': form}
    return render(request, 'restaurant/table_form.html', context)

def update_table(request, pk):
    table = Table.objects.get(number=pk)
    form = TableForm(instance=table)

    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('home')

    context = {'form': form}
    return render(request, 'restaurant/table_form.html', context)

def create_order(request, pk):
    form = OrderForm()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.table = Table.objects.get(number=pk)
            order.save()
        return redirect('home')

    context = {'form': form}
    return render(request, 'restaurant/order_form.html', context)

def view_table(request, pk):
    table = Table.objects.get(number=pk)
    orders = Order.objects.filter(table=table)
    context = {
        'table': table,
        'orders': orders
    }
    return render(request, 'restaurant/view_table.html', context)

def view_order(request, pk):
    order = Order.objects.get(pk=pk)
    context = {
        'order': order
    }
    return render(request, 'restaurant/view_order.html', context)