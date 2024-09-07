from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models.deletion import ProtectedError
from django.contrib import messages
from .models import *
import json
import os
# Create your views here.

# Index

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return render(request, "main/index.html")
    
# LogIn

def log_in(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Mauvais utilisateur ou inexistant")
            return redirect('login')
    else:
        return render(request, "main/login.html")

# LogOut

@login_required(login_url='/login')
def log_out(request):
    logout(request)
    return redirect('login')

# Dashboard

@login_required(login_url='/login')
def dashboard(request):
    context = {
        'customerCount': Customer.objects.filter(user=request.user).count(),
        'vehiculeCount': Vehicle.objects.filter(user=request.user).count(),
        'orderCount': Order.objects.filter(user=request.user).count(),
        'invoiceCount': Invoice.objects.filter(user=request.user).count()
    }
    return render(request, "dashboard/dashboard.html", context)

# Customer

@login_required(login_url='/login')
def customer(request):
    context = {
        'customers': Customer.objects.filter(user=request.user)
    }
    return render(request, 'customer/customer.html', context)

# View Customer

@login_required(login_url='/login')
def viewCustomer(request, customer_id):
    context = {
        'customer': Customer.objects.get(user=request.user, id=customer_id)
    }
    return render(request, "customer/viewCustomer.html", context)

# Add Customer

@login_required(login_url='/login')
def addCustomer(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        tva = request.POST.get('tva')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        new_customer = Customer(user=request.user, first_name=first_name, last_name=last_name, address=address, tva=tva, phone=phone, email=email)
        new_customer.save()
        messages.success(request, "Le client a été ajouté avec succès")
        return redirect('customer')
    else:
        context = {
            'actionStatus': 'Ajouter'
        }
        return render(request, "customer/handleCustomer.html", context)
    
# Edit Customer
    
@login_required(login_url='/login')
def editCustomer(request, customer_id):
    if request.method == 'POST':
        edit_customer = Customer.objects.get(user=request.user, id=customer_id)
        edit_customer.first_name = request.POST.get('first_name')
        edit_customer.last_name = request.POST.get('last_name')
        edit_customer.address = request.POST.get('address')
        edit_customer.tva = request.POST.get('tva')
        edit_customer.phone = request.POST.get('phone')
        edit_customer.email = request.POST.get('email')
        edit_customer.save()
        messages.success(request, "Le client a été modifié avec succès")
        return redirect('customer')
    else:
        context = {
            'actionStatus': 'Modifier',
            'customer': Customer.objects.get(user=request.user, id=customer_id)
        }
        return render(request, "customer/handleCustomer.html", context)

# Delete Customer

@login_required(login_url='/login')
def deleteCustomer(request, customer_id):
    delete_customer = Customer.objects.get(user=request.user, id=customer_id)
    try:
        delete_customer.delete()
        messages.success(request, "Le client a été supprimé avec succès")
    except ProtectedError:
        messages.error(request, "Le client ne peux pas être supprimé")
    return redirect('customer')

# Vehicle

@login_required(login_url='/login')
def vehicle(request):
    context = {
        'vehicles': Vehicle.objects.filter(user=request.user)
    }
    return render(request, 'vehicle/vehicle.html', context)

# View Vehicle

@login_required(login_url='/login')
def viewVehicle(request, vehicle_id):
    context = {
        'vehicle': Vehicle.objects.get(user=request.user, id=vehicle_id)
    }
    return render(request, "vehicle/viewVehicle.html", context)

# Add Vehicle

@login_required(login_url='/login')
def addVehicle(request):
    if request.method == 'POST':
        customer = Customer.objects.get(id=request.POST.get('customer'))
        model = CarModel.objects.get(id=request.POST.get('model'))
        number_plate = request.POST.get('number_plate')
        chassis = request.POST.get('chassis')
        circulation = request.POST.get('circulation')
        new_vehicle = Vehicle(user=request.user, customer=customer, model=model, number_plate=number_plate, chassis=chassis, circulation=circulation)
        new_vehicle.save()
        messages.success(request, "Le véhicule a été ajouté avec succès")
        return redirect('vehicle')
    else:
        context = {
            'actionStatus': 'Ajouter',
            'customers': Customer.objects.filter(user=request.user),
            'carmodels': CarModel.objects.all()
        }
        return render(request, "vehicle/handleVehicle.html", context)
    
# Edit Vehicle

@login_required(login_url='/login')
def editVehicle(request, vehicle_id):
    if request.method == 'POST':
        edit_vehicle = Vehicle.objects.get(user=request.user, id=vehicle_id)
        edit_vehicle.customer = Customer.objects.get(id=request.POST.get('customer'))
        edit_vehicle.model = CarModel.objects.get(id=request.POST.get('model'))
        edit_vehicle.number_plate = request.POST.get('number_plate')
        edit_vehicle.chassis = request.POST.get('chassis')
        edit_vehicle.circulation = request.POST.get('circulation')
        edit_vehicle.save()
        messages.success(request, "Le véhicule a été modifié avec succès")
        return redirect('vehicle')
    else:
        context = {
            'actionStatus': 'Modifier',
            'vehicle': Vehicle.objects.get(user=request.user, id=vehicle_id),
            'customers': Customer.objects.filter(user=request.user),
            'carmodels': CarModel.objects.all()
        }
        return render(request, "vehicle/handleVehicle.html", context)

# Delete Vehicle

@login_required(login_url='/login')
def deleteVehicle(request, vehicle_id):
    delete_vehicle = Vehicle.objects.get(user=request.user, id=vehicle_id)
    try:
        delete_vehicle.delete()
        messages.success(request, "Le véhicule a été supprimé avec succès")
    except ProtectedError:
        messages.error(request, "Le véhicule ne peut pas être supprimé")
    return redirect('vehicle')

# Order

def order(request):
    context = {
        'orders': Order.objects.filter(user=request.user)
    }
    return render(request, 'order/order.html', context)

# View Order

@login_required(login_url='/login')
def viewOrder(request, order_id):
    context = {
        'order': Order.objects.get(user=request.user, id=order_id)
    }
    return render(request, "order/viewOrder.html", context)

# Add Order

@login_required(login_url='/login')
def addOrder(request):
    if request.method == 'POST':
        vehicle = Vehicle.objects.get(id=request.POST.get('vehicle'))
        mileage = request.POST.get('mileage')
        intervention_value = request.POST.getlist('interventionItem')
        description = request.POST.get('description')
        new_order = Order(user=request.user, vehicle=vehicle, mileage=mileage, description=description)
        new_order.save()
        for orderValue in intervention_value:
            new_orderitem = OrderItem(name=orderValue)
            new_orderitem.save()
            new_order.order_item.add(new_orderitem)
        messages.success(request, "L'ordre de réparation a été ajouté avec succès")
        return redirect('order')
    else:
        context = {
            'actionStatus': 'Ajouter',
            'vehicles': Vehicle.objects.filter(user=request.user),
        }
        return render(request, "order/handleOrder.html", context)
    
# Edit Order

@login_required(login_url='/login')
def editOrder(request, order_id):
    if request.method == 'POST':
        edit_order = Order.objects.get(user=request.user, id=order_id)
        edit_order.vehicle = Vehicle.objects.get(id=request.POST.get('vehicle'))
        edit_order.mileage = request.POST.get('mileage')
        intervention_value = request.POST.getlist('interventionItem')
        edit_order.description = request.POST.get('description')
        old_order_items = list(edit_order.order_item.all())
        edit_order.order_item.clear()
        edit_order.save()
        for orderValue in intervention_value:
            new_orderitem = OrderItem(name=orderValue)
            new_orderitem.save()
            edit_order.order_item.add(new_orderitem)
        for old_item in old_order_items:
            if old_item not in edit_order.order_item.all():
                old_item.delete()
        messages.success(request, "L'ordre de réparation a été modifié avec succès")
        return redirect('order')
    else:
        context = {
            'actionStatus': 'Modifier',
            'order': Order.objects.get(user=request.user, id=order_id),
            'vehicles': Vehicle.objects.filter(user=request.user),
        }
        return render(request, "order/handleOrder.html", context)

# Delete Order

@login_required(login_url='/login')
def deleteOrder(request, order_id):
    delete_order = Order.objects.get(user=request.user, id=order_id)
    order_items = list(delete_order.order_item.all())
    try:
        delete_order.delete()
        for order_item in order_items:
            order_item.delete()
        messages.success(request, "L'ordre de réparation a été supprimé avec succès")
    except ProtectedError:
        messages.error(request, "L'ordre de réparation ne peut pas être supprimé")
    return redirect('order')

# Show Order

@login_required(login_url='/login')
def showOrder(request, order_id):
    context = {
        'order': Order.objects.get(user=request.user, id=order_id)
    }
    return render(request, "order/templateOrder.html", context)

# Invoice

@login_required(login_url='/login')
def invoice(request):
    context = {
        'invoices': Invoice.objects.filter(user=request.user)
    }
    return render(request, 'invoice/invoice.html', context)

# View Invoice

@login_required(login_url='/login')
def viewInvoice(request, invoice_id):
    context = {
        'invoice': Invoice.objects.get(user=request.user, id=invoice_id)
    }
    return render(request, "invoice/viewInvoice.html", context)

# Add Invoice

@login_required(login_url='/login')
def addInvoice(request, order_id):

    existing_invoice = Invoice.objects.filter(order=order_id).first()
    if existing_invoice:
        messages.error(request, "La facture existe déjà pour cette ordre de réparation.")
        return redirect('order')

    elif request.method == 'POST':
        order = Order.objects.get(id=order_id)
        discount = request.POST.get('discountTotal')
        totalHTVA = request.POST.get('HTVATotal')
        totalTVA = request.POST.get('TVATotal')
        totalTVAC = request.POST.get('amountTotal')
        status = request.POST.get('status')
        new_invoice = Invoice(user=request.user, order=order, discount=discount, totalHTVA=totalHTVA, totalTVA=totalTVA, totalTVAC=totalTVAC, status=status)
        new_invoice.save()
        intervention_value = request.POST.getlist('interventionItem')
        QuantityValue = request.POST.getlist('QuantityValue')
        UnitPriceValue = request.POST.getlist('UnitPriceValue')
        DiscountValue = request.POST.getlist('DiscountValue')
        AmountValue = request.POST.getlist('AmountValue')
        for nameData, quantityData, unitPriceData, discountData, amountData in zip(intervention_value, QuantityValue, UnitPriceValue, DiscountValue, AmountValue):
            new_invoiceitem = InvoiceItem(name=nameData, quantity=quantityData, unitPrice=unitPriceData, discount=discountData, amount=amountData)
            new_invoiceitem.save()
            new_invoice.invoice_item.add(new_invoiceitem)
        messages.success(request, "La facture a été ajouté avec succès")
        return redirect('invoice')
    else:
        context = {
            'actionStatus': 'Ajouter',
            'order': Order.objects.get(user=request.user, id=order_id)
        }
        return render(request, "invoice/handleInvoice.html", context)
    
# Edit Invoice

@login_required(login_url='/login')
def editInvoice(request, invoice_id):
    if request.method == 'POST':
        edit_invoice = Invoice.objects.get(user=request.user, id=invoice_id)
        edit_invoice.discount = request.POST.get('discountTotal')
        edit_invoice.totalHTVA = request.POST.get('HTVATotal')
        edit_invoice.totalTVA = request.POST.get('TVATotal')
        edit_invoice.totalTVAC = request.POST.get('amountTotal')
        edit_invoice.status = request.POST.get('status')
        intervention_value = request.POST.getlist('interventionItem')
        QuantityValue = request.POST.getlist('QuantityValue')
        UnitPriceValue = request.POST.getlist('UnitPriceValue')
        DiscountValue = request.POST.getlist('DiscountValue')
        AmountValue = request.POST.getlist('AmountValue')
        old_invoice_items = list(edit_invoice.invoice_item.all())
        edit_invoice.invoice_item.clear()
        edit_invoice.save()
        for nameData, quantityData, unitPriceData, discountData, amountData in zip(intervention_value, QuantityValue, UnitPriceValue, DiscountValue, AmountValue):
            new_invoiceitem = InvoiceItem(name=nameData, quantity=quantityData, unitPrice=unitPriceData, discount=discountData, amount=amountData)
            new_invoiceitem.save()
            edit_invoice.invoice_item.add(new_invoiceitem)
        for old_item in old_invoice_items:
            if old_item not in edit_invoice.invoice_item.all():
                old_item.delete()
        messages.success(request, "La facture a été modifié avec succès")
        return redirect('invoice')
    else:
        context = {
            'actionStatus': 'Modifier',
            'invoice': Invoice.objects.get(user=request.user, id=invoice_id),
        }
        return render(request, "invoice/handleInvoice.html", context)
    
# Delete Invoice

@login_required(login_url='/login')
def deleteInvoice(request, invoice_id):
    delete_invoice = Invoice.objects.get(user=request.user, id=invoice_id)
    invoice_items = list(delete_invoice.invoice_item.all())
    try:
        delete_invoice.delete()
        for invoice_item in invoice_items:
            invoice_item.delete()
        messages.success(request, "La facture a été supprimé avec succès")
    except ProtectedError:
        messages.error(request, "Le facture ne peut pas être supprimé")
    return redirect('invoice')

# Show Invoice

@login_required(login_url='/login')
def showInvoice(request, invoice_id):
    context = {
        'invoice': Invoice.objects.get(user=request.user, id=invoice_id)
    }
    return render(request, "invoice/templateInvoice.html", context)

# Reset Car Model With Json File 'carmodel.json'

@login_required(login_url='/login')
def resetCarModel(request):
    CarModel.objects.all().delete()
    json_path = os.path.join( 'json', 'carmodel.json')
    print(json_path)
    with open(json_path, 'r', encoding='utf-8') as json_file:
        car_data = json.load(json_file)
    for item in car_data:
        brand = item["brand"]
        models = item["models"]
        for model in models:
            car = CarModel.objects.create(
                brand=brand,
                model=model,
            )
            car.save()
    messages.success(request, "Car Model Reset")
    return redirect('dashboard')