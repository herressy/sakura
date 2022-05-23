from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import CreateView
from .models import Table, User, Meal, Order
from .forms import TableForm, OrderForm
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from pathlib import Path
import csv
import os

BASE_DIR = Path(__file__).resolve().parent.parent

def home(request):
    tables = Table.objects.all()
    context = {'tables': tables}
    return render(request, 'restaurant/home.html', context)

def login_page(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    
    context = {'form': form}
    return render(request, 'restaurant/login.html', context)

def logout_page(request):
    logout(request)
    return redirect('home')


def create_table(request):
    form = TableForm()
    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('home')

    context = {'form': form}
    return render(request, 'restaurant/table_form.html', context)

def view_table(request, pk):
    table = Table.objects.get(number=pk)
    orders = Order.objects.filter(table=table)
    context = {
        'table': table,
        'orders': orders
    }
    return render(request, 'restaurant/view_table.html', context)

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

def view_order(request, pk):
    order = Order.objects.get(pk=pk)
    context = {'order': order}
    return render(request, 'restaurant/view_order.html', context)

def create_basic_menu(request):
    """
    Clears meal objects and creates basic Sakura menu from csv
    files in sakura/menu.
    """
    Meal.objects.all().delete()
    menu_path = str(BASE_DIR) + '/menu/'
    for file in os.listdir(menu_path):
        if file.endswith('.csv'):
            file_abs_path = menu_path + file
            with open(file_abs_path, 'r') as f:
                reader = csv.DictReader(f, delimiter=';')
                for line in reader:
                    try:
                        name = line['NAME']
                        price = line['PRICE']
                        kind = file.rsplit('.')[0]
                        Meal.objects.create(
                            name=name,
                            price=price,
                            kind=kind,
                        )
                    except ValueError as Err:
                        print(str(Err).strip('.') + ' from ' + file)
                        continue
    return redirect('home')