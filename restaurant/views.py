from django.shortcuts import render, redirect, HttpResponse
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

from source.settings import BASE_DIR
import csv
import os


def home(request):
    tables = Table.objects.all()
    context = {'tables': tables}
    return render(request, 'restaurant/home.html', context)

def login_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    context = {'form': form}
    return render(request, 'restaurant/login_view.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')

def create_table(request):
    form = TableForm()
    errors = False
    if request.method == 'POST':
        form = TableForm(request.POST)
        table_number = request.POST.get('number')
        if Table.objects.filter(number=table_number).exists():
            messages.error(request, f'Table {table_number} is already in use!')
            errors = True
        if form.is_valid() and not errors:
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'restaurant/table_form.html', context)

def view_table(request, pk):
    table = Table.objects.get(pk=pk)
    orders = Order.objects.filter(table=table)
    context = {
        'table': table,
        'orders': orders
    }
    return render(request, 'restaurant/view_table.html', context)

def update_table(request, pk):
    table = Table.objects.get(pk=pk)
    form = TableForm(instance=table)
    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('home')
    context = {'form': form}
    return render(request, 'restaurant/table_form.html', context)

def delete_table(request, pk):
    table = Table.objects.get(pk=pk)
    table.soft_delete()
    for order in table.order_set.all():
        order.soft_delete()
    return redirect('home')

def create_order(request, pk):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.table = Table.objects.get(pk=pk)
            order.save()
        return redirect('home')
    context = {'form': form}
    return render(request, 'restaurant/order_form.html', context)

def view_order(request, pk):
    order = Order.objects.get(pk=pk)
    context = {'order': order}
    return render(request, 'restaurant/view_order.html', context)

def delete_order(request, pk):
    order = Order.objects.get(pk=pk)
    order.soft_delete()
    return redirect(request.META.get('HTTP_REFERER'))

def history_view(request, action):
    """
    Shows all soft-deleted orders.
    """
    orders = Order.all_objects.filter(deleted=True).all()
    if action == 'delete':
        orders.delete()
        messages.info(request, 'Orders history has been deleted.')
    context = {'orders': orders}
    return render(request, 'restaurant/orders_history.html', context)

def create_basic_menu(request):
    """
    Deletes meal objects and creates basic Sakura menu from csv
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
                        Meal.objects.create(
                            name=line['NAME'],
                            price=line['PRICE'],
                            kind=file.rsplit('.')[0]
                        )
                    except ValueError as Err:
                        print(str(Err).strip('.') + ' from ' + file)
                        continue
    return redirect('home')