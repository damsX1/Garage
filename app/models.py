from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class UserSettings(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    company_setup = models.BooleanField(default=False)
    invoice_counter = models.IntegerField(default=0)
    last_year = models.IntegerField(default=datetime.date.today().year)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.user.username

class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    tva = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=16)
    email = models.CharField(max_length=50, blank=True)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    tva = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=16)
    email = models.CharField(max_length=50, blank=True)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class CarModel(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.brand} {self.model}'

class Vehicle(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    model = models.ForeignKey(CarModel, on_delete=models.PROTECT)
    number_plate = models.CharField(max_length=20, unique=True)
    chassis = models.CharField(max_length=17, unique=True)
    circulation = models.DateField()
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    
    def __str__(self):
        return f'{self.number_plate} | {self.chassis}'
    
class OrderItem(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    order_item = models.ManyToManyField(OrderItem)
    mileage = models.CharField(max_length=10)
    description = models.TextField()
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    def __str__(self):
        return f"OR #{self.id}"
    
class InvoiceItem(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    unitPrice = models.CharField(max_length=100)
    discount = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Invoice(models.Model):
    StatusChoices = [
        ('paid', 'Payée'),
        ('unpaid', 'Non payé')
    ]

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    number_id = models.CharField(max_length=20, unique=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    invoice_item = models.ManyToManyField(InvoiceItem)
    discount = models.CharField(max_length=100)
    totalHTVA = models.CharField(max_length=100)
    totalTVA = models.CharField(max_length=100)
    totalTVAC = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=StatusChoices)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.number_id:
            year = datetime.date.today().year
            user_settings = UserSettings.objects.get(user=self.user)
            if user_settings.last_year != year:
                user_settings.invoice_counter = 0
                user_settings.last_year = year
            user_settings.invoice_counter += 1
            user_settings.save()
            self.number_id = f"{year}-{user_settings.invoice_counter:02d}"
        super().save(*args, **kwargs)
    def __str__(self):
        return f"Invoice #{self.id}"