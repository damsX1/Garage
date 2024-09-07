from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('login', log_in, name='login'),
    path('logout', log_out, name='logout'),

    path('dashboard', dashboard, name='dashboard'),

    path('customer', customer, name='customer'),
    path('viewcustomer/<int:customer_id>', viewCustomer, name='viewcustomer'),
    path('addcustomer', addCustomer, name='addcustomer'),
    path('editcustomer/<int:customer_id>', editCustomer, name='editcustomer'),
    path('deletecustomer/<int:customer_id>', deleteCustomer, name='deletecustomer'),

    path('vehicle', vehicle, name='vehicle'),
    path('viewvehicle/<int:vehicle_id>', viewVehicle, name='viewvehicle'),
    path('addvehicle', addVehicle, name='addvehicle'),
    path('editvehicle/<int:vehicle_id>', editVehicle, name='editvehicle'),
    path('deletevehicle/<int:vehicle_id>', deleteVehicle, name='deletevehicle'),

    path('order', order, name='order'),
    path('vieworder/<int:order_id>', viewOrder, name='vieworder'),
    path('addorder', addOrder, name='addorder'),
    path('editorder/<int:order_id>', editOrder, name='editorder'),
    path('deleteorder/<int:order_id>', deleteOrder, name='deleteorder'),
    path('showorder/<int:order_id>/', showOrder, name='showorder'),

    path('invoice', invoice, name='invoice'),
    path('viewinvoice/<int:invoice_id>', viewInvoice, name='viewinvoice'),
    path('addinvoice/<int:order_id>', addInvoice, name='addinvoice'),
    path('editinvoice/<int:invoice_id>', editInvoice, name='editinvoice'),
    path('deleteinvoice/<int:invoice_id>', deleteInvoice, name='deleteintervention'),
    path('showinvoice/<int:invoice_id>/', showInvoice, name='showinvoice'),
    
    path('resetcarmodel', resetCarModel, name='resetcarmodel'),
]