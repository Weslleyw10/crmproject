from django.contrib.auth import forms
from django.db.models import fields
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User

from django.contrib import messages

from .decorators import *

from .models import *
from .forms import *
from .filters import *


# Create your views here.
@login_required(login_url='login')
@admin_only
def home(request):
    lastFiveOrders = Order.objects.all().order_by('-status')[:5]
    orders = Order.objects.all().count()
    ordersDelivered = Order.objects.filter(status='Delivered').count()
    ordersPending = Order.objects.filter(status='Pending').count()

    customers = Customer.objects.all()

    context = {
        "orders": orders,
        "ordersDelivered": ordersDelivered,
        "ordersPending": ordersPending,
        "lastFiveOrders": lastFiveOrders,
        "customers": customers
    }

    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {"products":products})

@login_required(login_url='login')
def customers(request, pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()
    ordersTotal = orders.count()

    filters = OrderFilter(request.GET, queryset=orders)
    orders = filters.qs


    context = {
        "customer": customer,
        "orders": orders,
        "ordersTotal": ordersTotal,
        "filters": filters
    }

    return render(request, 'accounts/customers.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    orderFormSet = inlineformset_factory(Customer, Order, fields=('product','status'), extra=5)
    customer = Customer.objects.get(id=pk)
    formset = orderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer':customer})

    if request.method == 'POST':
        formset = orderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = { "formset": formset }
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = { "form":form }
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.status = 'Canceled'
        order.save()
        # order.delete()
        return redirect('/')

    context = {"item":order}
    return render(request, 'accounts/delete.html', context)

@unauthenticated_user
def loginSystem(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR Password is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutSystem(request):
    logout(request)
    return redirect('login')

@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for ' + username)

            return redirect('login')

    context = {"form": form}
    return render(request, 'accounts/register.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def profile(request):
    orders = request.user.customer.order_set.all().count()
    listOrders = request.user.customer.order_set.all()
    ordersDelivered = listOrders.filter(status='Delivered').count()
    ordersPending = listOrders.filter(status='Pending').count()

    context = {
        "orders": orders,
        "listOrders": listOrders,
        "ordersDelivered": ordersDelivered,
        "ordersPending": ordersPending
    }

    return render(request, 'accounts/profile.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def account(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {"form": form}
    return render(request, 'accounts/account.html', context)
